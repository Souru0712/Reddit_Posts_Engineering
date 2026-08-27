# Devvit Recon — Capture Sheet (Top → Year)

Source: `recon_corpus.json`, generated 2026-08-27 22:24 UTC.
50 searches (5 subs × 10 queries), phrase-quoted, `sort=top` `time=year`, 0 errors.
23 raw hits → 23 unique threads → **13 distinct chores**.

`Times seen` = independent threads. Cross-posts by the same author are counted
but flagged, because one requester posting twice is not two requests.

---

## Capture table

| # | Chore (in mods' own words) | Where seen | Times seen | Link |
|---|---|---|---|---|
| 1 | "is there a bot that has the ability to detect AI images and alert mods of what it finds" — plus a text-side variant, "we do not allow AI responses but it can be difficult to recognize them" | r/ModSupport (2026-04-15), r/ModSupport (2026-01-13), r/ModHelp (2025-11-06) | **3** | [img](https://www.reddit.com/r/ModSupport/comments/1sml7k5/) · [img](https://www.reddit.com/r/ModSupport/comments/1qc1mo1/) · [text](https://www.reddit.com/r/modhelp/comments/1oppzix/) |
| 2 | "any way to automatically inform users that they are shadowbanned using AutoModerator or another tool/bot… without manual intervention to redirect them to appeal" | r/ModSupport + r/ModHelp (both 2025-11-24) | 2 ⚠️ *same author, same day — 1 requester* | [1](https://www.reddit.com/r/ModSupport/comments/1p5jndg/) · [2](https://www.reddit.com/r/modhelp/comments/1p5jkn8/) |
| 3 | "our biggest problem is drive-by trolls… is there an app that will allow mods to restrict comments to only joined users who posted something first?" (crowd control leaks) | r/ModSupport (2026-06-17) | 1 | [link](https://www.reddit.com/r/ModSupport/comments/1u8dzd7/) |
| 4 | "he has no easy way to check things like bans, comments, removed posts, reviewqueue activity, etc. across all the communities he manages" — cross-sub mod analytics | r/Devvit (2025-12-08) | 1 ⚠️ *builder scoping, not a mod asking* | [link](https://www.reddit.com/r/Devvit/comments/1pgzctl/) |
| 5 | "I get the exact same question in modmail on a regular basis… It's silly that I'm trying to reply to these messages manually" — modmail auto-reply | r/ModSupport (2025-08-27) | 1 | [link](https://www.reddit.com/r/ModSupport/comments/1n1qnzk/) |
| 6 | "mod queue has an unmoderated post that was submitted by a now suspended account… is there an app that will auto remove those" | r/ModHelp (2026-01-09) | 1 | [link](https://www.reddit.com/r/modhelp/comments/1q8k7dv/) |
| 7 | "is there a bot that also does a reverse image search to catch spammers who are stealing images from instagram or elsewhere on the internet rather than just reposting from within reddit?" | r/ModHelp (2026-05-21) | 1 | [link](https://www.reddit.com/r/modhelp/comments/1tjvka3/) |
| 8 | "a bot or app that can automatically summarize replies in a thread and post that summary as a pinned comment… update as new comments come in" | r/ModHelp (2026-04-10) | 1 | [link](https://www.reddit.com/r/modhelp/comments/1shy443/) |
| 9 | "is there any way to automatically either spoiler tag a post or remove those without the tag" — timed around a game launch | r/ModSupport (2025-09-01) | 1 | [link](https://www.reddit.com/r/ModSupport/comments/1n5kj9a/) |
| 10 | "new account bot spam from a certain company, and I am not patient enough to play whack-a-mole… block a sentence or key words entirely" | r/ModSupport (2026-01-07) | 1 ⚠️ *automod regex likely covers this* | [link](https://www.reddit.com/r/ModSupport/comments/1q6egp5/) |
| 11 | "users frequently post links to another site and… fail to include title and author. Is there a bot that could pull this information and reply with a comment" | r/ModHelp (2026-02-08) | 1 ⚠️ *needs off-Reddit fetch per target site* | [link](https://www.reddit.com/r/modhelp/comments/1qywvrh/) |
| 12 | "How do other mods handle new accounts that get flagged by the reputation filter?" — manual verification-post workflow; corroborated by a mod logging "three hours in one day just catching up on verifications" and 180k actions/12mo | r/ModSupport (2026-06-02), r/ModSupport (2026-04-04) | 2 ⚠️ *1 request + 1 workload testimony* | [ask](https://www.reddit.com/r/ModSupport/comments/1tutqbo/) · [evidence](https://www.reddit.com/r/ModSupport/comments/1scdp69/) |
| 13 | "Is there a tool to block some web sites?" | r/ModHelp (2025-11-24) | 1 ❌ **DEAD — self-answered**: "I found it in Post and comments → link restrictions" | [link](https://www.reddit.com/r/modhelp/comments/1p5w7kf/) |

**12 live rows.** Row 13 is logged only so it isn't rediscovered.

---

## Incumbent intel (hard data point, from the corpus)

A Devvit repost app already ships and was announced in r/ModSupport on 2025-12-11:
**`identify-reposts`** — https://developers.reddit.com/apps/identify-reposts
Author: u/flattenedbricks. Pre-submission webview check, configurable image/text/link
thresholds, "Post Anyway" → modqueue.

Directly caps **row 7** — on-Reddit repost detection is taken. The surviving gap in
row 7 is *off-Reddit* reverse image search (Instagram, stolen content), which that
app explicitly does not do.

> The author's own framing is also the strongest workload quote in the corpus:
> "Reposts are one of the biggest drains on moderator time… mods spend hours cleaning it up."
> He spent **108 days** building it. Note that against your 40-hour scope discipline.

**The No-incumbent axis is otherwise UNSCORED.** Checking it requires the Devvit app
directory, which the recon harness does not read. Do that before scoring, per the
instrument — not from memory.

---

## Excluded (matched a phrase, not a chore)

| Thread | Why excluded |
|---|---|
| [Sub count limits open letter](https://www.reddit.com/r/ModSupport/comments/1scdp69/) | Policy essay. Mined for row 12 workload evidence only. |
| [u/SheTookMeToTheSky_26 seeking to moderate](https://www.reddit.com/r/needamod/comments/1vh1lzi/) | Mod recruitment. "don't have to spend hours daily" — phrase noise. |
| [r/r4rSydneysfw looking for mods](https://www.reddit.com/r/needamod/comments/1vhu8jt/) | Mod recruitment. Same phrase noise. |
| [Modding and Reddit Streaks](https://www.reddit.com/r/ModSupport/comments/1ou56b2/) | Admin feature request. Not app-addressable. |
| [Sub recommendation algorithm](https://www.reddit.com/r/ModSupport/comments/1p7agr9/) | Admin-only surface. Real wish, unbuildable by a third party. |
| [How do you report a subreddit?](https://www.reddit.com/r/ModSupport/comments/1s8rp7q/) | Admin function. Not app-addressable. |

---

## Coverage failure — read before scoring

**4 of 10 queries returned zero across all five subs**, and the instrument's designated
highest-yield pairing was one of them.

| Query | Total hits |
|---|---|
| `automod can't` | **0** |
| `automoderator can't` | **0** |
| `we do this manually` | **0** |
| `wish there was` | 1 (admin-only noise) |
| `how do you all handle` | 1 |
| `is there a bot that` | 5 |
| `is there a tool` | 5 |
| `spending hours` | 6 (5 of 6 noise) |
| `any way to automatically` | 3 |
| `is there an app that` | 2 |

**r/AutoModerator returned 0 hits on all 10 queries.** The sub the instrument calls
"Highest value" contributed nothing.

Two corrections this forces:

1. **The `automod can't` hypothesis is unvalidated, not disproven.** Phrase-quoting
   demands that exact contraction. Mods write "automod cannot", "automod doesn't",
   "automod won't", "can automod do X". Re-run unquoted before concluding anything.
2. **The real high-yield family is `is there a bot/tool/app that`** — 12 of 23 hits and
   nearly every genuine chore row. `spending hours` is the worst performer: it surfaces
   burnout narratives and mod-recruitment posts, not tool requests.

### The re-run that closes the 20-row gap

```bash
python recon.py --no-quote                      # widen all 10 queries
python recon.py --sort new                      # the instrument's second pass
python recon.py --time all --subreddits AutoModerator
```

Unquoted should move r/AutoModerator off zero on its own. If it stays at zero across
`--no-quote` and `--time all`, that sub is a dead channel and the instrument's
"Where to read" table needs rewriting.

---

## Distribution plan — named prospects

Real people with an open, unanswered request. Reply in-thread when the app ships.

| Username | Their request | Thread | Contacted? |
|---|---|---|---|
| u/kwikwon01 | Detect AI images, alert mods (NSFW couples verification) | https://www.reddit.com/r/ModSupport/comments/1sml7k5/ | No |
| u/myst3ryAURORA_green | Bot to scan a picture and reveal AI | https://www.reddit.com/r/ModSupport/comments/1qc1mo1/ | No |
| u/TheRealGuncho | Tool to recognize AI text responses | https://www.reddit.com/r/modhelp/comments/1oppzix/ | No |
| u/Mutthal8 | Auto-notify shadowbanned users | https://www.reddit.com/r/ModSupport/comments/1p5jndg/ | No |
| u/DarthWalker-34381 | Restrict comments to members who posted first | https://www.reddit.com/r/ModSupport/comments/1u8dzd7/ | No |
| u/Gojo_dev | Cross-sub mod analytics dashboard | https://www.reddit.com/r/Devvit/comments/1pgzctl/ | No |
| u/steamwhistler | Modmail auto-reply | https://www.reddit.com/r/ModSupport/comments/1n1qnzk/ | No |
| u/coopersoar | Auto-remove modqueue posts from suspended accounts | https://www.reddit.com/r/modhelp/comments/1q8k7dv/ | No |
| u/pixiefarm | Reverse image search vs off-Reddit sources | https://www.reddit.com/r/modhelp/comments/1tjvka3/ | No |
| u/Baconkings | Auto-summarize thread into pinned comment | https://www.reddit.com/r/modhelp/comments/1shy443/ | No |
| u/average_sk_player | Auto-spoiler tagging | https://www.reddit.com/r/ModSupport/comments/1n5kj9a/ | No |
| u/SuMianAi | Block a whole sentence, not just keywords | https://www.reddit.com/r/ModSupport/comments/1q6egp5/ | No |
| u/royal_rose_ | Link enrichment bot | https://www.reddit.com/r/modhelp/comments/1qywvrh/ | No |
| u/WombatHat42 | New-account verification handling | https://www.reddit.com/r/ModSupport/comments/1tutqbo/ | No |

u/flattenedbricks (identify-reposts) is not a prospect — he is the incumbent.
