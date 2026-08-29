# Devvit Recon — Decision

Corpora in `data/output/`. This file is the scoring pass and the scope freeze.

---

## Verdict: build the flair enforcement fix. Option B is dead.

The chore-noun sweep across all five subs, `top`/`year`, closed both open questions.

---

## Gate 1 — ANSWERED by the corpus. The native toggle is broken, and mods say so.

`require post flair` returned **18 threads in 12 months** (r/ModSupport 12, r/ModHelp 6)
from ~14 distinct mods. The titles are the evidence:

| Date | Sub | Thread |
|---|---|---|
| 2026-06-27 | ModSupport | **"Users are able to post without flair even though I have toggled on 'require post flair'"** |
| 2026-06-08 | ModSupport | "Require Post Flair not working?" |
| 2026-06-17 | ModSupport | "Has reddit removed flairs being mandatory?" |
| 2026-06-01 | ModHelp | "How to Require Post Flair Like this Subreddit?" (15 comments) |
| 2026-04-16 | ModHelp | "Post rules not being applied" |
| 2026-03-16 | ModSupport | "How are people avoiding post flairs before posting?" |
| 2026-02-13 | ModSupport | "HOW DO I ENFORCE POST FLAIR" |
| 2026-01-01 | ModHelp | "Subreddit set to require post flairs, but some users can't set flair" |
| 2025-11-16 | ModSupport | "Require flair for every post not working" |
| 2025-09-24 | ModHelp | "Automod and post flair requirement don't seem to funciton" |

Plus 8 more. **The 2020 leak u/sveltegamine reported is still leaking in 2026.**

### This reframes the product

We scoped a *grace period* — a kinder alternative to a blunt removal. That is not what
these mods are asking for. They turned the native setting **on** and it **does not work**.

> **You are not selling kindness. You are selling the flair requirement that actually works.**

That is a materially stronger pitch and it raises conversion. A mod who has already flipped
the toggle and watched unflaired posts arrive anyway is pre-qualified: they have the
problem, they tried the official fix, it failed, and they went to a support sub about it.

---

## Gate 2 — directory results

### Option B is dead. Not competitive — saturated.

| App | Installs | |
|---|---|---|
| **Modqueue Pruner** — *"Periodically removes posts and comments from the mod queue for deleted, suspended or shadowbanned users"* | **428** | Word-for-word Option B |
| Suspended Remove — *"silently removes content from suspended or shadowbanned accounts… Zero configuration"* | 60 | Same chore again |
| Modqueue Nuke | 1386 | Purge by age/reports/score/keyword |
| Modqueue Tools | 364 | Queue analytics |
| Subreddit Status | 230 | Queue monitoring |
| Modqueue Alerts / Toolbox Notes Pruner / +5 more | 72 / 25 / — | |

Twelve apps on the modqueue. **Drop Option B entirely.**

### Option A's niche is open

`unflaired` · `grace period` · `delayed` · `cleanup` · `stale` · `flair reminder`
→ **all empty.**

One correction to my earlier claim: Devvit apps *do* act on elapsed time — Modqueue Pruner
is "periodic", and Auto-Highlights *"removes them when they expire"* (3 installs). The
elapsed-time trigger is not novel. **What is unoccupied is flair enforcement specifically.**

### AssistantBOT is alive — the one real competitor

`u/AssistantBOT1` last active **2026-08-17**. r/AssistantBOT: 591 subscribers, last post
2024-11 *"Bots have been moved to a more powerful system."*

This is the bot r/AutoModerator's auto-response officially recommends for flair enforcement.
It is running. But it is beatable:

- **Not a Devvit app.** It does not appear in the directory, cannot be one-click installed,
  and does not count toward anyone's Developer Funds. Install friction is mod-invite plus
  wiki config versus a directory button.
- **Discovery has failed.** Eighteen mods hit this problem in the last year and not one of
  those titles mentions AssistantBOT. Whatever it does, mods are not finding it.
- **591 subscribers** on its own sub after years.

---

## What the sweep did NOT support

**Row 19 (modmail auto-reply) is disconfirmed, and my hypothesis was wrong.** I argued its
frequency of 1 was a query artifact. Given a chore-noun query set, `modmail auto response`
returned **0** and `automate modmail` returned 1 — a Devvit product announcement, i.e. a
false positive. The demand is not there. Row 19 drops.

Seven of ten chore queries returned zero in the year window: `modmail auto response`,
`remove unflaired posts`, `modqueue backlog`, `clear the modqueue`, `verify new users`,
`detect ban evasion`, `pin a comment automatically`.

`schedule a post` returned 12 — Reddit's *native scheduler* is also visibly broken
("Unable to schedule a post", "Schedule a post not working", "No longer able to schedule
posts in the mobile app?"). Real pain, but 5+ Devvit scheduler apps already serve it. Skip.

---

## Scoring — the chosen row

| Axis | Score | Evidence |
|---|---|---|
| Frequency | **3** | 18 threads, 12 months, ~14 mods, still live |
| Breadth | **3** | Any subreddit using post flair; no genre or NSFW skew |
| Automod gap | **3** | r/AutoModerator's own macro: *"AutoModerator is not able to do this"* |
| No incumbent | **2** | Nothing in the Devvit directory; AssistantBOT exists off-platform |
| Build size | **3** | Scheduler + flair check + comment. Weekend-scoped |
| | **14 / 15** | |

Comfortably past the kill threshold of 12.

---

## v1 — frozen

> **Enforce post flair reliably: detect posts that are still unflaired after a configurable
> delay, comment telling the author how to fix it, then remove. Restore automatically if
> flair is added.**

Positioning is the native toggle's failure, not kindness: *"Require Post Flair, except it
actually works."*

Not in v1: the other five row-1 sub-asks, day-of-week rules, OP-engagement timers.

### One open technical question — spike before writing features

Can an author set flair on their own **removed** post, and does a flair-change event fire
for removed content? If either is no, use **filter** instead of remove at T+delay: the post
sits in modqueue, stays recoverable, and the restore path never has to work.

---

## Named prospects — all live, all 2026 unless noted

Reply in these threads when the app ships. This is the highest-conversion distribution move
available and it is entirely async.

| Username | Thread | Sub |
|---|---|---|
| u/Organic-Concept4760 | Users able to post without flair despite the toggle | ModSupport |
| u/Wolfpiresnow | How to Require Post Flair Like this Subreddit? (15c) | ModHelp |
| u/RxMurloc | Require Post Flair not working? | ModSupport |
| u/RidsBabs | Has reddit removed flairs being mandatory? | ModSupport |
| u/DoubleFistMeRaw | HOW DO I ENFORCE POST FLAIR | ModSupport |
| u/x-LeananSidhe-x | How are people avoiding post flairs before posting? | ModSupport |
| u/Soul-Burn | Set to require post flairs, but some users can't set flair | ModHelp |
| u/allthroat247 | Required flair | ModSupport |
| u/DrTankHead | Most effective way to auto-flair support posts | ModSupport |
| u/therealamberrose | Post rules not being applied | ModHelp |
| u/Casinoroyale008 | Postflair question | ModSupport |
| u/r2girls | Require flair for every post not working (2025-11) | ModSupport |
| u/Ok-Huckleberry5836 | Can't seem to disable "No Flair" option (2025-10) | ModSupport |
| u/jfb3 | Automod and post flair requirement don't function (2025-09) | ModHelp |

**Read first, do not cold-pitch:** u/tired_of_the_woes, *"Making Flairs Mandatory (solution,
2026)"* (ModHelp, 2026-07-23) and u/brentspine, *"Updated 2025: Require post flair"*
(ModHelp, 2025-10). These publish the current workaround. They are either your competition
or your best allies — know what they recommend before you ship.

---

## Note on the failed probe run

`flair_probe.py`'s first run screened 120 subs and returned **zero** — it looked for an
`is_flair_required` key that `post_requirements()` does not return. My defect. The script now
measures behaviour instead (share of flaired posts per sub, unflaired rate bucketed by post
age) and dumps the real endpoint keys so nothing is guessed twice. Raw failed run kept at
`data/output/flair_probe_failed_run.json`.

Gate 1 no longer depends on it — the corpus answered it. Re-running is now confirmatory:
it would quantify *how much* leaks and how fast mods clean up, which is pitch material
rather than a go/no-go.
