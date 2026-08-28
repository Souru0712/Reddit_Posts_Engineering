# Devvit Recon — Scoring & Build Decision

Corpus and chore rows: `RECON_CAPTURE.md` (58 threads, 23 live chores).
This file is the scoring pass and the scope freeze.

---

## Gate checks

### Gate 1 — Does Reddit natively require post flair? **Answered, with a wrinkle**

⚠️ *Second-hand.* `support.reddithelp.com`, `mods.reddithelp.com`, `mod.reddit.com`
and `developers.reddit.com` are all blocked at this environment's egress proxy. The
findings below come from search-engine summaries of those pages plus one third-party
guide — not from pages actually fetched. **Confirm in mod settings.**

Three findings, and the order matters:

1. **No native "require post flair" toggle.** Mods enable post flair under Content and
   Controls, then enforce the requirement with AutoModerator.
   ([guide](https://blog.devvyy.xyz/blog/2025/reddit/how-to-make-post-flairs-required/))
2. **But AutoModerator already covers the hard version.** A `flair_text: ""` rule removes
   unflaired posts at submission. Every sub already has this available.
3. **AutoModerator cannot cover the soft version.** Per Reddit's own AutoModerator help
   page: *"AutoModerator can only act on new posts, comments, reports or edits, and
   cannot delay an action"* — and it *"cannot act on old or past content."*
   ([Reddit mod help](https://mods.reddithelp.com/hc/en-us/articles/360002561632-AutoModerator))

**Net effect on row 1:** your predicted downgrade lands, but on a different axis than
expected. Automod-gap **stays at 3** — the delay is structurally impossible and Reddit
documents it in those words. What takes the hit is conversion, exactly as you called it:
the competitor is not a native toggle, it is the automod rule the sub already runs. The
pitch is *"kinder than the blunt removal you already have,"* not *"you need this."*

The corpus asked for precisely the soft version, seven years ago and unprompted:
> *"Would it be possible to have automod say delete a post after 2 minutes if it has not
> been assigned a flair yet? If automod can't do it is there some other way?"*
> — r/AutoModerator, 2019-01-16

### Gate 2 — Devvit app directory sweep: **NOT COMPLETED. Still owed.**

`developers.reddit.com` is blocked at egress and a general web search is not the app
directory. The only app I independently surfaced was
[shiruken/only-flairs](https://github.com/shiruken/only-flairs), which corroborates your
row 17 finding. **No timed-removal app appeared — but absence from a web search is not
absence from the directory, and I will not report this gate as passed.**

Search the directory yourself for: `scheduler`, `timer`, `delayed`, `grace period`,
`flair reminder`, `unflaired`. Do it before writing code.

---

## Scoring — `want × conversion` (adopted)

Your reframing is right and it replaces the rubric's Breadth axis. An incumbent doesn't
reduce want; it removes installs from the winnable pool. Recording it as scored:

| Row | Chore | Want | Conv | **Realized** | Binding constraint |
|---|---|---|---|---|---|
| **1** | **Delayed post re-check** | 3 | **3** | **9** | Remove/flair permissions only; one primitive, six asks |
| **19** | **Modmail auto-reply** | 3 | **3** | **9** | Small build, modest permissions — *frequency is a query artifact* |
| 6 | Act on report reasons | 2 | 3 | 6 | Skews to subs organized enough to configure custom reports |
| 5 | Ban / mute / rate-limit | 3 | 2 | 6 | Scariest permission ask on the platform |
| 17 | Restrict commenting | 2 | 2 | 4 | Near-substitute ships (Only Flairs) |
| 2 | Image analysis | 3 | **1** | 3 | Per-image inference cost; false positives break the 7-day hold |
| 9 | Account verification | 3 | **1** | 3 | Demand concentrates NSFW → fails the monetization gate |
| 3 | Mod-action triggers | 1 | 2 | 2 | Largely occupied (FlairAssistant, FlairGuard) |
| 21 | Auto-spoiler | 1 | 2 | 2 | Launch-driven; cannot hold 7 consecutive days |
| 13 | Automod sandbox | 3 | **0** | **0** | Used once while writing a rule, never installed. Website, not an app |

### Row 19 and the query artifact

Not a market signal — an instrument defect, and mine to own. None of the ten queries
contained a chore noun: no *modmail*, *flair*, *queue*, *sticky*, *verification*. They
were all generic tool-request patterns, so they could only find demand phrased as a
generic tool request. A frequency of 1 on modmail measures the query set, not the market.
Row 11 is likely affected the same way.

**Fixed in the harness.** `recon.py --queryset chore` runs ten chore-noun queries
(`automate modmail`, `remove unflaired posts`, `require post flair`, `clear the modqueue`,
`verify new users`, …); `--queryset both` runs all twenty. Run it before treating any
frequency-of-1 row as settled.

---

## Incumbent register

| App | Covers | Effect |
|---|---|---|
| FlairAssistant | Actions on mod-set flair, incl. removal reasons and banning | Row 3 largely occupied |
| FlairGuard | Same trigger model + lock, modmail, temp ban, mod dashboard | Row 3 largely occupied |
| [Only Flairs](https://github.com/shiruken/only-flairs) | Restricts commenting to flaired users | Row 17 near-substitute |
| identify-reposts | On-Reddit repost detection, pre-submission webview | Row 2 on-Reddit half |

**Row 1 survives.** All three flair apps fire on a **mod action**. Row 1 fires on
**elapsed time with no action** — a trigger none of them have. That distinction is the
product.

**Positioning consequence:** flair-heavy subs already run a flair app. You are asking for
a second one. Lead with the timer, not with flair.

---

## v1 scope — frozen, pending Gate 2

> **Timed removal of unflaired posts: a configurable grace period, a warning comment, and
> auto-restore when the author adds flair.**

The other five sub-asks under row 1 are the roadmap if installs come. They are not v1.
The "one primitive serves six asks" framing is true, and it is exactly the framing that
turns a weekend into 108 days.

### Open technical risk — spike this before committing

**Auto-restore is the unverified half, and it carries the whole pitch.** The warn-and-
remove half is plainly buildable: a scheduler plus a flair check. Restore requires two
things nobody has confirmed:

1. **Can an author set flair on their own removed post?** If the flair editor is
   unavailable once a post is removed, auto-restore is impossible by construction.
2. **Does a flair-change event fire for removed content?** Devvit exposes a post-flair
   trigger; whether it fires on removed posts is unknown.

If either answer is no, the tool degrades to *automod with a delay* — a materially weaker
pitch, because the kindness you are selling is the restore, not the wait.

**Cheaper design that sidesteps both:** at T+grace, **filter** instead of remove. The post
lands in modqueue, stays recoverable by a human, and the restore path never has to work.
Worth testing against the remove-and-restore version before committing to either.

One hour of spiking answers all of this. Do it after Gate 2, before scope freeze.
