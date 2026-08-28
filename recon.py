"""Devvit Recon — Week 1 capture harness.

Runs the exact search queries from the recon instrument across the recon
subreddits, sorted Top -> Year, dedupes hits across queries, and emits:

  data/output/recon_corpus.json   full records (feed this back for clustering)
  data/output/recon_capture.md    capture table + distribution plan, prefilled

Read-only: uses client_id + client_secret only. No account password needed.

    export REDDIT_CLIENT_ID=... REDDIT_CLIENT_SECRET=...
    python recon.py

Credentials also resolve from config/config.conf [api_keys] if env is unset.
"""
import argparse
import configparser
import json
import os
import sys
from datetime import datetime, timezone

import praw
import prawcore

# From the instrument: "Where to read"
SUBREDDITS = [
    "AutoModerator",
    "ModSupport",
    "ModHelp",
    "needamod",
    "Devvit",
]

# From the instrument: "Exact search queries" — verbatim, order preserved.
QUERIES = [
    "is there a bot that",
    "is there an app that",
    "is there a tool",
    "automod can't",
    "automoderator can't",
    "any way to automatically",
    "wish there was",
    "how do you all handle",
    "we do this manually",
    "spending hours",
]

# Chore-noun queries. The generic set above contains no chore nouns — no
# "modmail", "flair", "queue", "sticky" — so it can only find demand that
# happens to be phrased as a generic tool request. This set tests for demand
# the other one structurally cannot see.
CHORE_QUERIES = [
    "automate modmail",
    "modmail auto response",
    "remove unflaired posts",
    "require post flair",
    "modqueue backlog",
    "clear the modqueue",
    "verify new users",
    "detect ban evasion",
    "pin a comment automatically",
    "schedule a post",
]

QUERY_SETS = {
    "tool": QUERIES,
    "chore": CHORE_QUERIES,
    "both": QUERIES + CHORE_QUERIES,
}

USER_AGENT = "python:devvit-recon:0.1 (week-1 capture, read-only)"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "output")


def load_credentials():
    cid = os.environ.get("REDDIT_CLIENT_ID")
    secret = os.environ.get("REDDIT_CLIENT_SECRET")
    if cid and secret:
        return cid, secret

    conf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "config.conf")
    parser = configparser.ConfigParser()
    if parser.read(conf) and parser.has_section("api_keys"):
        cid = cid or parser.get("api_keys", "reddit_client_id", fallback=None)
        secret = secret or parser.get("api_keys", "reddit_secret_key", fallback=None)

    if not cid or not secret or cid.startswith("["):
        sys.exit(
            "Missing Reddit credentials.\n"
            "  export REDDIT_CLIENT_ID=... REDDIT_CLIENT_SECRET=...\n"
            "or fill [api_keys] in config/config.conf "
            "(create one at https://www.reddit.com/prefs/apps, type: script)."
        )
    return cid, secret


def search(reddit, subreddit, query, sort, time_filter, limit, quote):
    """Return raw hits for one (subreddit, query) pair, restricted to that sub."""
    term = f'"{query}"' if quote else query
    hits = []
    for post in reddit.subreddit(subreddit).search(
        term, sort=sort, time_filter=time_filter, limit=limit
    ):
        hits.append(
            {
                "id": post.id,
                "subreddit": subreddit,
                "title": post.title,
                "author": str(post.author) if post.author else "[deleted]",
                "score": int(post.score),
                "num_comments": int(post.num_comments),
                "created_utc": datetime.fromtimestamp(
                    post.created_utc, tz=timezone.utc
                ).strftime("%Y-%m-%d"),
                "link": f"https://www.reddit.com{post.permalink}",
                "selftext": (post.selftext or "").strip().replace("\r", ""),
                "over_18": bool(post.over_18),
            }
        )
    return hits


def cell(text, width=None):
    """Make a string safe for a markdown table cell."""
    flat = " ".join((text or "").split()).replace("|", "\\|")
    if width and len(flat) > width:
        flat = flat[: width - 1].rstrip() + "…"
    return flat


def render_markdown(posts, meta):
    lines = []
    lines.append("# Devvit Recon — Week 1 capture")
    lines.append("")
    lines.append(
        f"Generated {meta['generated']} · sort=`{meta['sort']}` · "
        f"time=`{meta['time_filter']}` · phrase-quoted=`{meta['quote']}`"
    )
    lines.append("")
    lines.append(
        f"{meta['searches']} searches ({len(meta['subreddits'])} subreddits × "
        f"{len(meta['queries'])} queries, set='{meta['queryset']}') · "
        f"{meta['raw_hits']} raw hits · **{len(posts)} unique threads**"
    )
    lines.append("")
    if meta["errors"]:
        lines.append("**Search errors:**")
        for err in meta["errors"]:
            lines.append(f"- `r/{err['subreddit']}` × `{err['query']}` → {err['error']}")
        lines.append("")

    lines.append("## Hits per subreddit × query")
    lines.append("")
    subs, queries = meta["subreddits"], meta["queries"]
    lines.append("| Query | " + " | ".join(f"r/{s}" for s in subs) + " |")
    lines.append("|---|" + "---|" * len(subs))
    for q in queries:
        row = [str(meta["grid"].get(f"{s}|{q}", 0)) for s in subs]
        lines.append(f"| `{q}` | " + " | ".join(row) + " |")
    lines.append("")

    lines.append("## Capture table")
    lines.append("")
    lines.append(
        "One row per thread, ordered by how many distinct queries surfaced it "
        "(the crude relevance proxy). Collapse rows that describe the same chore "
        "before scoring — `Times seen` below is *query hits on this thread*, not "
        "chore frequency across threads."
    )
    lines.append("")
    lines.append("| # | Chore (thread title) | Where seen | Times seen | Link |")
    lines.append("|---|---|---|---|---|")
    for i, p in enumerate(posts, 1):
        lines.append(
            f"| {i} | {cell(p['title'], 110)} | r/{p['subreddit']} "
            f"({p['created_utc']}, {p['num_comments']}c) | {len(p['matched_queries'])} "
            f"| {p['link']} |"
        )
    lines.append("")

    lines.append("## Distribution plan — named prospects")
    lines.append("")
    lines.append("| Username | Their request | Thread | Contacted? |")
    lines.append("|---|---|---|---|")
    for p in posts:
        if p["author"] == "[deleted]":
            continue
        lines.append(
            f"| u/{p['author']} | {cell(p['title'], 90)} | {p['link']} | No |"
        )
    lines.append("")

    lines.append("## Matched queries per thread")
    lines.append("")
    for i, p in enumerate(posts, 1):
        qs = ", ".join(f"`{q}`" for q in p["matched_queries"])
        lines.append(f"{i}. [{cell(p['title'], 100)}]({p['link']}) — r/{p['subreddit']} — {qs}")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Devvit recon capture harness")
    ap.add_argument("--sort", default="top", choices=["top", "new", "relevance", "comments"])
    ap.add_argument("--time", dest="time_filter", default="year",
                    choices=["hour", "day", "week", "month", "year", "all"])
    ap.add_argument("--limit", type=int, default=100, help="max hits per query (default 100)")
    ap.add_argument("--no-quote", dest="quote", action="store_false",
                    help="search loose terms instead of the exact phrase")
    ap.add_argument("--queryset", default="tool", choices=sorted(QUERY_SETS),
                    help="tool: the original 10 generic patterns (default); "
                         "chore: 10 chore-noun queries; both: all 20")
    ap.add_argument("--subreddits", nargs="*", default=SUBREDDITS)
    args = ap.parse_args()

    cid, secret = load_credentials()
    reddit = praw.Reddit(client_id=cid, client_secret=secret, user_agent=USER_AGENT)
    reddit.read_only = True

    by_id = {}
    grid = {}
    errors = []
    raw_hits = 0
    searches = 0

    queries = QUERY_SETS[args.queryset]

    for sub in args.subreddits:
        for query in queries:
            searches += 1
            try:
                hits = search(reddit, sub, query, args.sort, args.time_filter,
                              args.limit, args.quote)
            except (prawcore.exceptions.PrawcoreException, Exception) as exc:  # noqa: BLE001
                errors.append({"subreddit": sub, "query": query, "error": f"{type(exc).__name__}: {exc}"})
                print(f"  r/{sub:<14} {query!r:<28} ERROR {type(exc).__name__}", file=sys.stderr)
                continue

            grid[f"{sub}|{query}"] = len(hits)
            raw_hits += len(hits)
            print(f"  r/{sub:<14} {query!r:<28} {len(hits):>3} hits")

            for hit in hits:
                existing = by_id.get(hit["id"])
                if existing:
                    if query not in existing["matched_queries"]:
                        existing["matched_queries"].append(query)
                else:
                    hit["matched_queries"] = [query]
                    by_id[hit["id"]] = hit

    posts = sorted(
        by_id.values(),
        key=lambda p: (-len(p["matched_queries"]), -p["num_comments"], -p["score"]),
    )

    meta = {
        "generated": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "sort": args.sort,
        "time_filter": args.time_filter,
        "quote": args.quote,
        "queryset": args.queryset,
        "queries": queries,
        "subreddits": list(args.subreddits),
        "searches": searches,
        "raw_hits": raw_hits,
        "grid": grid,
        "errors": errors,
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    json_path = os.path.join(OUT_DIR, "recon_corpus.json")
    md_path = os.path.join(OUT_DIR, "recon_capture.md")

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "posts": posts}, fh, indent=2, ensure_ascii=False)
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(render_markdown(posts, meta))

    print(f"\n{searches} searches · {raw_hits} raw hits · {len(posts)} unique threads")
    if errors:
        print(f"{len(errors)} search errors (see markdown)")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
