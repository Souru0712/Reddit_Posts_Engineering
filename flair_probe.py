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


def flair_required(subreddit):
    """True/False, or None if the requirement could not be read."""
    try:
        req = subreddit.post_requirements()
    except Exception:
        return None
    for key in ("is_flair_required", "isFlairRequired"):
        if key in req:
            return bool(req[key])
    return None


def sample_subreddit(subreddit, limit):
    now = datetime.now(timezone.utc).timestamp()
    rows = []
    for post in subreddit.new(limit=limit):
        if getattr(post, "stickied", False):
            continue
        rows.append({
            "age_min": max(0.0, (now - post.created_utc) / 60.0),
            "flaired": bool(getattr(post, "link_flair_text", None)),
        })
    return rows


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
    ap.add_argument("--out", default="flair_probe")
    args = ap.parse_args()

    cid, secret = load_credentials()
    reddit = praw.Reddit(client_id=cid, client_secret=secret, user_agent=USER_AGENT)
    reddit.read_only = True

    print("=== GATE 2: AssistantBOT ===")
    bot = check_assistantbot(reddit)
    for k, v in bot.items():
        print(f"  {k}: {v}")

    print(f"\n=== GATE 1: screening subreddits for required flair ===")
    if args.subreddits:
        names = list(args.subreddits)
    else:
        names = []
        for sr in reddit.subreddits.popular(limit=args.subs):
            names.append(sr.display_name)

    required, not_required, unknown, nsfw_skipped = [], [], [], []
    for name in names:
        try:
            sr = reddit.subreddit(name)
            if getattr(sr, "over18", False):
                nsfw_skipped.append(name)          # payout needs SFW anyway
                continue
            state = flair_required(sr)
        except Exception as exc:  # noqa: BLE001
            unknown.append((name, f"{type(exc).__name__}"))
            continue
        if state is True:
            required.append(name)
        elif state is False:
            not_required.append(name)
        else:
            unknown.append((name, "no is_flair_required key"))

    screened = len(required) + len(not_required)
    print(f"  screened {screened} SFW subs · flair required in {len(required)}"
          f" ({100*len(required)/screened:.0f}%)" if screened else "  screened 0")
    print(f"  skipped: {len(nsfw_skipped)} NSFW, {len(unknown)} unreadable")

    print(f"\n=== GATE 1: unflaired rate by post age, in flair-required subs ===")
    tally = {label: {"total": 0, "unflaired": 0} for _, label in BUCKETS}
    per_sub = {}
    for name in required:
        try:
            rows = sample_subreddit(reddit.subreddit(name), args.posts)
        except Exception as exc:  # noqa: BLE001
            print(f"  r/{name}: sample failed ({type(exc).__name__})")
            continue
        sub_unflaired = sum(1 for r in rows if not r["flaired"])
        per_sub[name] = {"sampled": len(rows), "unflaired": sub_unflaired}
        for r in rows:
            b = bucket_for(r["age_min"])
            tally[b]["total"] += 1
            if not r["flaired"]:
                tally[b]["unflaired"] += 1
        print(f"  r/{name:<24} {sub_unflaired:>3}/{len(rows):<3} unflaired")

    print(f"\n  {'age':<10}{'posts':>8}{'unflaired':>12}{'rate':>8}")
    for _, label in BUCKETS:
        t = tally[label]
        rate = (100 * t["unflaired"] / t["total"]) if t["total"] else 0
        print(f"  {label:<10}{t['total']:>8}{t['unflaired']:>12}{rate:>7.1f}%")

    fresh = tally["<15m"]
    old = tally[">24h"]
    fresh_rate = (100 * fresh["unflaired"] / fresh["total"]) if fresh["total"] else None
    old_rate = (100 * old["unflaired"] / old["total"]) if old["total"] else None

    print("\n=== VERDICT ===")
    if fresh_rate is None or old_rate is None:
        print("  Inconclusive — not enough posts in the extreme buckets. Raise --subs.")
    elif fresh_rate < 2 and old_rate < 2:
        print(f"  Native flair requirement HOLDS ({fresh_rate:.1f}% fresh, "
              f"{old_rate:.1f}% old). Option A is dead — go to Option B.")
    elif fresh_rate > old_rate + 5:
        print(f"  Setting LEAKS and mods clean up ({fresh_rate:.1f}% fresh → "
              f"{old_rate:.1f}% old). That gap is the chore. Option A is ALIVE.")
    else:
        print(f"  Leaks but nobody cleans up ({fresh_rate:.1f}% fresh, "
              f"{old_rate:.1f}% old). Weak felt pain — treat Option A as unproven.")

    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{args.out}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({
            "generated": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "assistantbot": bot,
            "screened": screened,
            "flair_required": required,
            "flair_not_required": not_required,
            "nsfw_skipped": nsfw_skipped,
            "unknown": unknown,
            "buckets": tally,
            "per_sub": per_sub,
        }, fh, indent=2)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
