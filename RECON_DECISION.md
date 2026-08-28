# Devvit Recon — Scoring & Build Decision

Corpus: `RECON_CAPTURE.md` (58 threads) + `data/output/automod_chore_corpus.json`
(17 threads, chore-noun sweep). This file is the scoring pass and the scope decision.

---

## ⚠️ Gate 1 — CORRECTED. My earlier answer was wrong.

**I previously reported there is no native "require post flair" toggle.** That came from a
third-party blog and a search-engine summary. The corpus now contradicts it from three
independent primary sources:

| Thread | Date | What it says |
|---|---|---|
| [8860hi](https://www.reddit.com/r/AutoModerator/comments/8860hi/) | 2018-03 | *"reddit's redesign having a setting for required post flairs"* |
| [guu20t](https://www.reddit.com/r/AutoModerator/comments/guu20t/) | 2020-06 | Names the exact path: *Mod Tools > Post Flair Settings > … > Post Requirements > require post flair set to on* |
| [10kh06f](https://www.reddit.com/r/AutoModerator/comments/10kh06f/) | 2023-01 | *"I require post flair on all of the posts in my sub"* — working |

**The native toggle exists.** What matters now is the failure mode u/sveltegamine reports
immediately after switching it on:

> *"However we are still getting posts that do not have flair… I asked one person who was
> posting, if they could tell me what they were posting from, and they replied that they
> were on mobile. I also know a fair amount of people on my sub use old reddit."*

So the native setting **leaks** — old reddit and older mobile clients bypass it. That was
true in 2020. **Whether it still leaks in 2026 is now the single question that decides
this build**, and it is not answerable from the corpus.

### The find that reframes everything

[djpoq5](https://www.reddit.com/r/AutoModerator/comments/djpoq5/) (2019, u/dequeued)
publishes r/AutoModerator's own **auto-response macros**. One is a purpose-built regex for
flair-enforcement questions — its trigger list includes `delay`, `period`, `hours?`,
`minutes?`, `time`. The canned reply:

> *"AutoModerator is not able to do this. AutoModerator evaluates content as it's being
> posted. Since link flair cannot be set until* after *a submission is already posted…
> submissions often not have link flair when AutoModerator is looking at it.*
> *Additionally, AutoModerator is not able to review content after time has passed.
> AutoModerator can only evaluate something when it's created, edited, or reported, and at
> no other times.*
> *To enforce link flair requirements, you will need a custom bot. Check out /r/AssistantBOT."*

Three things follow, and they cut in different directions:

1. **My "automod already covers the hard version" claim was also wrong.** A `flair_text: ""`
   removal at submit time produces *false removals*, because on old reddit and mobile the
   flair is set after posting. The automod workaround is broken for this use case, and
   r/AutoModerator says so in an automated reply. **Row 1's conversion goes back up** — the
   competitor is not a working automod rule.
2. **The question is asked often enough that the sub automated the answer.** A community
   only writes a macro for a question it is tired of answering. That is stronger frequency
   evidence than any thread count in this corpus.
3. **A named incumbent surfaces: r/AssistantBOT.** A pre-Devvit bot the sub officially
   recommends for exactly this chore. Its current status is unknown and must be checked.

---

## Gate 2 — Devvit directory: partially complete

Searched: `scheduler`, `timer`, `delayed`, `grace period`, `unflaired`.

| Search | Result |
|---|---|
| `delayed` | **Nothing found** |
| `grace period` | **Nothing found** |
| `unflaired` | **Nothing found** |
| `scheduler` | 5 apps — all *post publishing*, not delayed re-check |
| `timer` | 3 apps — one relevant |

### What is occupied

| App | Installs | Blocks |
|---|---|---|
| **OP Reply Enforcer (reply-timer)** — *"cascading timers for initial community responses and mandatory OP replies"* | **3** | Row 1 sub-ask "remove if OP doesn't engage" — the TipOfMyTongue chore. Weak adoption. |
| **Flair Scheduler** — *"Allow a flair to be used only on a certain day or set of days"* | **84** | Row 1 sub-ask "restrict content by day-of-week" |
| Image Post Scheduler *(Winner – Best New Mod Tool)* | 384 | Nothing of ours — publishes scheduled content |
| schedulerplus / Scheduler / EpisodeScheduler | 61 / 10 / 5 | Nothing of ours — same category |

**Critical distinction: every "Scheduler" app publishes content at a time. None of them
re-checks an existing post after a delay.** Those are different products that share a word.

### What is still clear

**No app matched `unflaired`, `grace period`, or `delayed`.** The v1 as scoped has no
directory incumbent.

### Still unsearched — do these

`suspended` · `modqueue` · `cleanup` · `flair reminder` · `stale` · `expire`

These cover row 1 sub-asks 4 and 6, which were never checked.

---

## Install-count calibration — read this before committing to 50

The screenshots give real adoption numbers, and they reset expectations:

| Percentile of what's visible | Installs |
|---|---|
| Award-winning mod tool (Image Post Scheduler) | 384 |
| Solid mid-tier (Flair Scheduler) | 84 |
| Typical (schedulerplus) | 61 |
| Long tail (Scheduler, EpisodeScheduler, OP Reply Enforcer) | 10, 5, 3 |

**Your target of 50 qualifying installs lands between the 61 and 84 tier.** That is roughly
top-quartile for a Devvit mod tool, and it is ~13% of what a category-winning app achieved.
Achievable, but it is not the low bar the "50" number makes it sound like. Most apps in this
directory never reach 10.

---

## Chore-noun sweep — what it did and did not settle

Run: r/AutoModerator only, `time=all`. **17 threads. 5 of 10 queries returned zero.**

| Query | Hits | Read |
|---|---|---|
| `schedule a post` | 10 | All about automod's *scheduled posts* feature — syntax help and debugging. Different chore. Native scheduled posts + 5 Devvit apps now cover it. **Dead.** |
| `require post flair` | 3 | **Gold.** All three are the Gate 1 evidence above. |
| `remove unflaired posts` | 2 | Both genuine; one is a plain "help me write this rule" |
| `modqueue backlog` | 1 | The dequeued macro post — the most valuable single hit in the corpus |
| `automate modmail` | 1 | False positive (a `{{permalink}}` bug report) |
| `modmail auto response`, `clear the modqueue`, `verify new users`, `detect ban evasion`, `pin a comment automatically` | **0** | — |

**Row 19 remains untested.** This run covered r/AutoModerator only; modmail chatter lives in
r/ModSupport and r/ModHelp. The primary sweep — all five subs, `top`/`year` — has not been
run, and it is the only one that can produce prospects.

---

## Revised recommendation

The flair v1 is now **contingent**, not confirmed. Native require-post-flair exists; the
whole value rests on whether it still leaks in 2026.

### Option A — original v1, contingent on one test

> Timed removal of unflaired posts: configurable grace period, warning comment, auto-restore
> on flair.

Alive **only if** the native toggle still leaks. If Reddit closed that hole, the surviving
market is subs with heavy old-reddit traffic plus mods who prefer a grace period to a hard
block — a much smaller pool than we scored.

### Option B — the sub-ask nobody has checked, and it may be better

> Clear modqueue entries whose author has since been suspended, deleted, or banned.

Why it may beat Option A now:

- **Zero false-positive risk.** A suspended account's post is unambiguously actionable. Nothing
  to get wrong, no angry mod thread, so it holds the 7-day window.
- **Remove-only permissions.** The cheapest possible install ask.
- **Invisible to users.** No user-facing behavior means no community backlash surface.
- **Topic-neutral.** Every sub with a modqueue, no genre skew, no NSFW concentration.
- **Live 2026 demand** — u/coopersoar, r/ModHelp, Jan 2026, still open.
- **Native alternative: none known.** Automod cannot act after time passes.

Its weakness is lower emotional salience — nobody writes an angry post about modqueue lint —
which usually means lower organic discovery.

**I would not choose between these until the two tests below are done.** They are cheap and
they decide it.

---

## Next actions, in order

1. **Test the native flair leak (20 min, decides Option A).** Enable Post Requirements →
   require post flair in a test sub. Then try to submit without flair from (a) old.reddit.com,
   (b) the official mobile app, (c) new reddit. **Any successful unflaired post = Option A is
   alive.** All three blocked = Option A is dead, go to Option B.
2. **Check r/AssistantBOT (10 min).** Is it still running? If yes, it is a direct incumbent
   with years of head start. If it is dead, that is a vacuum *and* a migration pitch.
3. **Finish the directory sweep (10 min).** Search `suspended`, `modqueue`, `cleanup`,
   `stale`, `expire`, `flair reminder`. This is the Gate 2 check for Option B.
4. **Run the primary chore sweep** — `python recon.py --queryset chore` across all five subs.
   Still the only outstanding source of named prospects.
5. **Then freeze scope**, and only then spike the auto-restore question (whether an author can
   flair their own removed post, and whether a flair event fires for removed content).

Steps 1–3 are 40 minutes total and they determine what gets built.
