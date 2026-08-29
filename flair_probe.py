"""Gate checks 1 and 2 — automated, read-only.

GATE 1: Does Reddit's native "require post flair" setting actually hold in 2026?

  Rather than posting from three clients and getting one anecdote, this samples
  live subreddits, keeps the ones with flair required, and measures what share
  of their newest posts are unflaired — bucketed by post age.

  The age buckets are the whole point:
    unflaired high when fresh, ~0 when old  -> the setting LEAKS and mods are
                                               manually cleaning up. That gap is
                                               the chore. Option A is alive.
    unflaired ~0 in every bucket            -> the setting HOLDS. Option A dead.
    unflaired high in every bucket          -> it leaks but nobody cleans up.
                                               No felt pain, so no demand.

GATE 2: Is AssistantBOT — the bot r/AutoModerator points mods to for flair
        enforcement — still running?

    export REDDIT_CLIENT_ID=... REDDIT_CLIENT_SECRET=...
    python flair_probe.py
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

import praw
import prawcore

from recon import load_credentials

USER_AGENT = "python:devvit-recon-flairprobe:0.1 (gate check, read-only)"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "output")

# (upper bound in minutes, label)
BUCKETS = [(15, "<15m"), (60, "15-60m"), (360, "1-6h"), (1440, "6-24h"),
           (float("inf"), ">24h")]


def bucket_for(age_min):
    for upper, label in BUCKETS:
        if age_min < upper:
            return label
    return BUCKETS[-1][1]


def requirement_keys(subreddit):
    """Diagnostic: what does post_requirements actually return? Guessing a key
    name is what broke the first run, so dump the truth instead."""
    try:
        return sorted(subreddit.post_requirements().keys())
    except Exception as exc:  # noqa: BLE001
        return [f"<{type(exc).__name__}>"]


def sample_subreddit(subreddit, limit):
    """Rows for one subreddit's newest posts, plus its overall flair rate.

    A sub whose posts are almost all flaired is one where flair is effectively
    required — whatever the settings say. That behavioural test needs no
    endpoint and cannot break on a renamed field.
    """
    now = datetime.now(timezone.utc).timestamp()
    rows = []
    for post in subreddit.new(limit=limit):
        if getattr(post, "stickied", False):
            continue
        rows.append({
            "age_min": max(0.0, (now - post.created_utc) / 60.0),
            "flaired": bool(getattr(post, "link_flair_text", None)),
        })
    rate = (sum(1 for r in rows if r["flaired"]) / len(rows)) if rows else 0.0
    return rows, rate


def check_assistantbot(reddit):
    """Gate 2: last visible activity of the bot and its subreddit."""
    out = {}
    for name in ("AssistantBOT", "AssistantBOT1"):
        try:
            user = reddit.redditor(name)
            last_c = next(iter(user.comments.new(limit=1)), None)
            last_s = next(iter(user.submissions.new(limit=1)), None)
            stamps = [x.created_utc for x in (last_c, last_s) if x]
            out[f"u/{name}"] = {
                "exists": True,
                "last_activity": (
                    datetime.fromtimestamp(max(stamps), tz=timezone.utc).strftime("%Y-%m-%d")
                    if stamps else None),
                "comment_karma": getattr(user, "comment_karma", None),
            }
        except Exception as exc:  # noqa: BLE001
            out[f"u/{name}"] = {"exists": False, "error": f"{type(exc).__name__}: {exc}"}

    try:
        sub = reddit.subreddit("AssistantBOT")
        newest = next(iter(sub.new(limit=1)), None)
        out["r/AssistantBOT"] = {
            "exists": True,
            "subscribers": sub.subscribers,
            "newest_post": (
                datetime.fromtimestamp(newest.created_utc, tz=timezone.utc).strftime("%Y-%m-%d")
                if newest else None),
            "newest_title": newest.title if newest else None,
        }
    except Exception as exc:  # noqa: BLE001
        out["r/AssistantBOT"] = {"exists": False, "error": f"{type(exc).__name__}: {exc}"}
    return out


def main():
    ap = argparse.ArgumentParser(description="Gate 1 + Gate 2 checks")
    ap.add_argument("--subs", type=int, default=120,
                    help="how many popular subreddits to screen (default 120)")
    ap.add_argument("--posts", type=int, default=100,
                    help="posts sampled per qualifying subreddit (default 100)")
    ap.add_argument("--subreddits", nargs="*",
                    help="screen these subreddits instead of the popular listing")
    ap.add_argument("--threshold", type=float, default=0.80,
                    help="min share of flaired posts for a sub to count as "
                         "flair-enforcing (default 0.80)")
    ap.add_argument("--out", default="flair_probe")
    args = ap.parse_args()

    cid, secret = load_credentials()
    reddit = praw.Reddit(client_id=cid, client_secret=secret, user_agent=USER_AGENT)
    reddit.read_only = True

    print("=== GATE 2: AssistantBOT ===")
    bot = check_assistantbot(reddit)
    for k, v in bot.items():
        print(f"  {k}: {v}")

    print("\n=== GATE 1: what post_requirements actually exposes ===")
    probe_keys = {}
    for name in ("AskReddit", "movies", "DnD"):
        try:
            probe_keys[name] = requirement_keys(reddit.subreddit(name))
        except Exception as exc:  # noqa: BLE001
            probe_keys[name] = [f"<{type(exc).__name__}>"]
        print(f"  r/{name}: {probe_keys[name]}")

    print("\n=== GATE 1: sampling subreddits ===")
    if args.subreddits:
        names = list(args.subreddits)
    else:
        names = [sr.display_name for sr in reddit.subreddits.popular(limit=args.subs)]

    enforcing, loose, nsfw_skipped, failed = [], [], [], []
    tally = {label: {"total": 0, "unflaired": 0} for _, label in BUCKETS}
    per_sub = {}

    for name in names:
        try:
            sr = reddit.subreddit(name)
            if getattr(sr, "over18", False):
                nsfw_skipped.append(name)          # payout requires SFW anyway
                continue
            rows, rate = sample_subreddit(sr, args.posts)
        except Exception as exc:  # noqa: BLE001
            failed.append((name, type(exc).__name__))
            continue
        if not rows:
            continue
        per_sub[name] = {"sampled": len(rows), "flair_rate": round(rate, 3)}
        if rate < args.threshold:
            loose.append(name)
            continue
        enforcing.append(name)
        for r in rows:
            b = bucket_for(r["age_min"])
            tally[b]["total"] += 1
            if not r["flaired"]:
                tally[b]["unflaired"] += 1

    print(f"  sampled {len(per_sub)} SFW subs · "
          f"{len(enforcing)} enforce flair (>={args.threshold:.0%} flaired) · "
          f"{len(loose)} do not")
    print(f"  skipped {len(nsfw_skipped)} NSFW, {len(failed)} errored")

    print(f"\n=== GATE 1: unflaired rate by post age, in flair-enforcing subs ===")
    print(f"  {'age':<10}{'posts':>8}{'unflaired':>12}{'rate':>8}")
    for _, label in BUCKETS:
        t = tally[label]
        rate = (100 * t["unflaired"] / t["total"]) if t["total"] else 0
        print(f"  {label:<10}{t['total']:>8}{t['unflaired']:>12}{rate:>7.1f}%")

    fresh, old = tally["<15m"], tally[">24h"]
    fresh_rate = (100 * fresh["unflaired"] / fresh["total"]) if fresh["total"] else None
    old_rate = (100 * old["unflaired"] / old["total"]) if old["total"] else None

    print("\n=== VERDICT ===")
    if fresh_rate is None or old_rate is None:
        print("  Inconclusive — empty age bucket. Raise --subs or --posts.")
    elif fresh_rate < 2 and old_rate < 2:
        print(f"  Flair enforcement HOLDS ({fresh_rate:.1f}% fresh, {old_rate:.1f}% old).")
        print("  No grace-period gap to sell into.")
    elif fresh_rate > old_rate + 5:
        print(f"  Enforcement LEAKS and mods clean up ({fresh_rate:.1f}% fresh -> "
              f"{old_rate:.1f}% old).")
        print("  That decay is the manual chore. A grace-period tool has a market.")
    else:
        print(f"  Leaks but nobody cleans up ({fresh_rate:.1f}% fresh, {old_rate:.1f}% old).")
        print("  No felt pain. Treat the chore as unproven.")

    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{args.out}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({
            "generated": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "assistantbot": bot,
            "post_requirements_keys": probe_keys,
            "threshold": args.threshold,
            "flair_enforcing": enforcing,
            "flair_loose": loose,
            "nsfw_skipped": nsfw_skipped,
            "failed": failed,
            "buckets": tally,
            "per_sub": per_sub,
        }, fh, indent=2)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
