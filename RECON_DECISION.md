# Devvit Recon — Decision

Corpora in `data/output/`. This file is the scoring pass and the scope freeze.

---

## ⚠️ STATUS: SCOPE UNFROZEN — 2026-08-30

A non-moderator alt account was blocked from posting unflaired on **both new reddit and
old reddit**: *"Your post must contain post flair."* The native toggle **held** in both
desktop clients.

That contradicts the premise this build was frozen on. See "Alt-account test" below.
**Do not write code until the mobile case is tested.**

---

## Earlier verdict (now in doubt): build the flair enforcement fix. Option B is dead.

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

**Must-have config, found while testing:** `exempt_moderators`, defaulting to **on**.
Reddit's native post requirements do not apply to moderators, and automod's convention is
`moderators_exempt: true`. Without this, the first thing a mod team sees after installing is
their own posts being removed. This also means the leak **cannot be reproduced from a
moderator account** — testing it needs a non-mod alt.

Not in v1: the other five row-1 sub-asks, day-of-week rules, OP-engagement timers.

### The restore question is smaller than I first stated

I raised two blockers. One dissolves on inspection, and the other only picks a UX.

**Blocker 1 — "does a flair-change event fire for removed posts?" — deleted.** The product
is already a periodic job. That same tick can re-check previously-removed posts for newly
added flair and approve them. No event subscription is needed at all.

**Blocker 2 — "can an author flair their own removed post?" — decides UX, not viability**,
because there is a design that never asks them to:

| | Flow | Needs the author to flair a removed post? |
|---|---|---|
| **UX A** | Remove → author adds flair normally → next tick restores | Yes |
| **UX B** | Remove → app comments the flair list → author replies `Discussion` → app sets the flair itself and approves | **No** |

The app holds mod permissions, so in UX B it sets flair on the author's behalf. UX B ships
regardless of the answer. UX A is nicer when available.

**If time is short, build UX B and skip the test entirely.**

### Alt-account test, 2026-08-30 — the toggle did NOT leak on desktop

Non-moderator alt, `Require Post Flair` on, submitting with no flair:

| Client | Result |
|---|---|
| New reddit (desktop web) | **Blocked** — "Add flair and tags*" + *"Your post must contain post flair."* |
| Old reddit (desktop web) | **Blocked** — "*choose a flair (none) [select]" + *"Your post must contain post flair."* |

**Both desktop clients enforced it correctly.** The leak was not reproduced.

#### What this does and does not settle

It does **not** dispose of the 18 corpus threads — those are real mods reporting real
failures through 2026. But it means the failure is not where we assumed.

**Untested, and it is the case the evidence actually points at:** the official **mobile
apps**. u/brentspine's line was *"Seems to only work on Desktop"* — and both clients tested
here are desktop. The one client class the claim names is the one not exercised.

Other unexamined explanations for the 18 threads: crossposts, third-party or API clients,
or misconfiguration where flairs are mod-only so users cannot self-assign (which is
literally u/Soul-Burn's thread, *"some users can't set flair"*).

#### Consequence for UX A vs UX B

**The question is moot for now.** Both were designs for restoring a post removed for
missing flair. If unflaired posts cannot be submitted in the first place, there is little
to remove and the product has no job. UX B remains the correct design *if* the chore
survives — it just is not what decides anything today.

### Earlier finding — an author cannot flair a removed post

Tested 2026-08-29 on a removed post, viewed as its author: **no flair control exists
anywhere** — not in the post's `...` menu (Edit post body / Save / Hide / Language /
Delete / spoiler / NSFW / brand affiliate / reply notifications), and not inside the edit
flow either.

An author cannot add flair to their own removed post. **UX A is impossible. Build UX B**,
where the app sets the flair itself after the author replies with a name.

Unrelated observation from the same session: the leak could not be reproduced from a
moderator account, since post requirements exempt moderators. That does not affect the
corpus evidence — those 18 reports concern ordinary users — but a marketing screenshot of
an unflaired post landing while the toggle is on needs a non-mod alt.

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

### The two "solution" threads — read, and they are not competitors

Both just say *flip the native toggle*. Neither ships a tool. And the second one confirms
the leak in the author's own words:

- [Making Flairs Mandatory (solution, 2026)](https://www.reddit.com/r/modhelp/comments/1v47apj/making_flairs_mandatory_solution_2026/)
  — u/tired_of_the_woes, 2026-07-23. Four steps: Mod Tools → Posts & Comments → Require
  Post Flair → toggle on. Scored **0**.
- [Updated 2025: Require post flair](https://www.reddit.com/r/modhelp/comments/1oj8hoj/updated_2025_require_post_flair/)
  — u/brentspine, 2025-10-29. Same instruction, plus: **"Seems to only work on Desktop."**

That line is the product. The native toggle is desktop-only; mobile and old reddit walk
straight past it. It is stated flatly by a mod who went looking, in October 2025.

brentspine also notes he posted it *because search did not surface an answer* — and that
r/AutoModerator's auto-response points at an outdated thread. **Discovery for this problem
is broken**, which favours a directory-listed app.

Two further evidence threads he links, not in our corpus:
[ModSupport 1g707qh](https://www.reddit.com/r/ModSupport/comments/1g707qh/how_do_i_make_post_flair_mandatory/) ·
[ModHelp 1afagnx](https://www.reddit.com/r/modhelp/comments/1afagnx/how_do_you_make_tags_and_flair_required_on_a/)

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
