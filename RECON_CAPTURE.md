# Devvit Recon — Capture Sheet (merged, 2 sweeps)

| Sweep | Scope | Config | Hits |
|---|---|---|---|
| **A** | r/ModSupport, r/ModHelp, r/needamod, r/Devvit, r/AutoModerator | `top` / `year` / quoted | 23 threads |
| **B** | r/AutoModerator only | `top` / **`all`** / quoted | 35 threads |

58 threads → **23 live chores + 1 dead.** Past the 20-row gate.

➡️ **Scoring, incumbent register and the v1 scope freeze live in `RECON_DECISION.md`.**
Rows 3 and 17 are now known to be incumbent-occupied; see that file before scoring them.

`Times seen` = independent threads. Same-author cross-posts flagged, not double-counted.

---

## ⚠️ Read before scoring: the two sweeps are not interchangeable

Sweep B is `time=all`. **Zero of its 35 threads fall inside the last 12 months** —
newest is 2025-07-18. Year-by-year: 2020 (6), 2021 (7), 2022 (6), 2023 (3),
2024 (1), 2025 (1), last 12mo (**0**).

Two consequences you must carry into scoring:

1. **Staleness risk on every B row.** A "automod can't do X" from 2021 may have been
   solved since — Reddit has shipped native scheduled posts, link restrictions, crowd
   control, ban-evasion and reputation filters in that window. **Verify the Automod-gap
   axis against current automod docs before scoring any B row.** Row 24 is already a
   confirmed casualty of exactly this.
2. **B rows are useless for the distribution plan.** You cannot convert by replying to a
   2021 thread. Named prospects come from sweep A only.

**r/AutoModerator is an archive, not a live channel.** It is the best source in the
corpus for *what automod structurally cannot do*, and the worst for *finding people to
sell to*. Your instrument's "Where to read" table should be split along that line.

---

## Capture table

| # | Chore | Automod gap (mods' words) | Where | Seen | Sw |
|---|---|---|---|---|---|
| **1** | **Delayed / scheduled re-check of a post** — remove if OP doesn't engage; remove unflaired after N min; restrict content by day-of-week; act when author deletes account; act after mod approves; clear modqueue posts from suspended accounts | *"automod can't tell time"* · *"automod can't do anything after the post has made it through"* | AutoModerator ×5, ModHelp ×1 | **6** | A+B |
| **2** | **Image content analysis** — detect AI-generated images (×2); reverse image search vs off-Reddit sources (×1); spam URLs embedded in image pixels (×1) | *"automoderator can't analyze the content of a picture"* | ModSupport ×2, ModHelp ×1, AutoModerator ×1 | **4** | A+B |
| **3** | **React to mod actions / export the mod log** — set flair when removal reason chosen; post to a private sub on each ban; POST ban/removal events to an external API | automod has no mod-action trigger | AutoModerator ×3 | **3** | B |
| **4** | **Recurring content posting from a source** — cycle a URL list daily; auto-post newest YouTube episode weekly; editable daily post | *"if automod can't do this, are there alternatives?"* | AutoModerator ×3 | 3 ⚠️ *all 2016-18; native Scheduled Posts likely covers* | B |
| **5** | **Ban / mute / rate-limit a user** — auto-ban minors who self-declare age; temp-block a comment spammer on first hit | *"automod can't ban users"* | AutoModerator ×2 | **2** | B |
| **6** | **Read and act on report reasons** — remove at N reports *for a specific rule*; let a bot's custom report trigger a filter | *"Automod can give report reasons but it can't read them and then act"* | AutoModerator ×2 | **2** | B |
| **7** | **Arithmetic / length thresholds** — enforce a minimum word count; run a formula on user input | *"automod can't be 'coded'… no loops, or variables"* — one mod generated **350 rules** with a Python script to fake a word counter | AutoModerator ×2 | **2** | B |
| **8** | **Rule chaining / thread state** — "has automod already commented here?"; continue after a remove action | *"after the first execution automod can't do anything else"* | AutoModerator ×2 | **2** | B |
| **9** | **New-account verification workflow** — manual verification-post review for flagged accounts | corroborated by a mod logging *"three hours in one day just catching up on verifications"*, 180k actions/12mo | ModSupport ×2 | **2** | A |
| **10** | **Notify shadowbanned users → appeal** | *"any way to automatically inform users that they are shadowbanned"* | ModSupport + ModHelp | 2 ⚠️ *same author, same day = 1 requester* | A |
| **11** | **Auto-flair unflaired posts by content rules** — filters run before flair, so filtered posts never get flaired | *"Surely there must be a better way?"* | AutoModerator | 1 | B |
| **12** | **React to a post hitting r/all or popular** — preemptively sticky a rules reminder before the wave arrives | *"automod can't do this today, but it's a really serious limitation"* | AutoModerator | 1 | B |
| **13** | **Automod rule sandbox / tester** — a regexr-like tool to test rules without live test posts | *"would eliminate half the need to ask questions here in /r/automoderator"* | AutoModerator | 1 ⚠️ *high breadth, but is it an install?* | B |
| **14** | **Dynamic link to the current stickied post** in an automod comment | no dynamic sticky reference exists | AutoModerator | 1 | B |
| **15** | **Crosspost tracking** — where was this crossposted, by whom | — | AutoModerator | 1 | B |
| **16** | **Detect AI-generated text** | *"we do not allow AI responses but it can be difficult to recognize them"* | ModHelp | 1 | A |
| **17** | **Restrict commenting to members who posted first** — drive-by trolls slip past crowd control | *"is there an app that will allow mods to restrict comments to only joined users who posted something first?"* | ModSupport | 1 | A |
| **18** | **Cross-sub mod analytics dashboard** | *"no easy way to check bans, comments, removed posts, reviewqueue activity across all the communities he manages"* | Devvit | 1 ⚠️ *builder scoping, not a mod asking* | A |
| **19** | **Modmail auto-reply to a repeated question** | *"It's silly that I'm trying to reply to these messages manually"* | ModSupport | 1 | A |
| **20** | **Auto-summarize a thread into a pinned comment**, updating as replies arrive | — | ModHelp | 1 | A |
| **21** | **Auto-spoiler tagging / remove untagged** around a launch | — | ModSupport | 1 | A |
| **22** | **Block a multi-word phrase**, not just keywords | *"not patient enough to play whack-a-mole"* | ModSupport | 1 ⚠️ *automod regex likely covers* | A |
| **23** | **Link enrichment** — pull title/author from a linked site, reply as comment | — | ModHelp | 1 | A |
| ~~24~~ | ~~Block some websites~~ | ❌ **DEAD** — self-answered: *"I found it in Post and comments → link restrictions"* | ModHelp | 1 | A |

### Leads (evidence, not requests — do not score)

- **Unicode / homoglyph evasion of keyword filters** — *"unicode characters (which automod cant read)"*, r/AutoModerator 2024. Real and broad, but no one asked for a tool.
- **Decisions using content other than the item examined** (parent comment, user history) — cited from the official [things Automoderator can't do](https://www.reddit.com/r/automoderator/wiki/no_can_do) wiki, r/AutoModerator 2017. Structural, still true as far as the corpus shows.

### Excluded from sweep B (9 threads)

User-error debugging (×4), automod-can-already-do-it (×2), an accidental phrase match
("I jokingly blocked automoderator. Can't unblock it."), an automod flair quirk, and
auto-downvoting the spam filter — which the API terms bar regardless of feasibility.

---

## My read on row 1

Row 1 is the standout on your rubric and I'd start scoring there:

- **Frequency** — 6 threads, 2019 → 2026, six distinct authors, two subs. Nothing else is close.
- **Automod gap** — structural, not a config problem. Automod is submit-time only and cannot tell time. Mods say so in those words, repeatedly, across seven years.
- **Breadth** — the sub-asks are topic-neutral. Unflaired-post cleanup and OP-engagement enforcement apply to essentially any subreddit with flairs or questions.
- **Build size** — one primitive (a scheduler + a re-check job) serves all six asks. Plausibly a weekend.
- **No incumbent** — **UNSCORED. Yours to check against the Devvit app directory.**

Rows 2 and 5 are the runners-up. Row 2 has the strongest *recent* demand (3 of its 4 threads are 2026) but needs an image model, which is not a weekend. Row 5 is clean and narrow.

---

## Incumbent intel (from sweep A)

**`identify-reposts`** — https://developers.reddit.com/apps/identify-reposts
u/flattenedbricks, announced r/ModSupport 2025-12-11. Pre-submission webview,
configurable image/text/link thresholds, "Post Anyway" → modqueue.

Caps on-Reddit repost detection. The surviving gap in row 2 is *off-Reddit* reverse
image search, which it explicitly does not do.

> His own framing: *"Reposts are one of the biggest drains on moderator time… mods
> spend hours cleaning it up."* He spent **108 days** on it. Weigh that against your
> 40-hour scope discipline.

**The No-incumbent axis is unscored across every row.** The harness does not read the
app directory. Check it before scoring, per your instrument — not from memory.

---

## Distribution plan — named prospects

Sweep A only. Sweep B threads are 2016–2023; those accounts are cold and replying there
converts nothing.

| Username | Their request | Thread | Contacted? |
|---|---|---|---|
| u/kwikwon01 | Detect AI images, alert mods | https://www.reddit.com/r/ModSupport/comments/1sml7k5/ | No |
| u/myst3ryAURORA_green | Bot to scan a picture and reveal AI | https://www.reddit.com/r/ModSupport/comments/1qc1mo1/ | No |
| u/TheRealGuncho | Tool to recognize AI text | https://www.reddit.com/r/modhelp/comments/1oppzix/ | No |
| u/Mutthal8 | Auto-notify shadowbanned users | https://www.reddit.com/r/ModSupport/comments/1p5jndg/ | No |
| u/DarthWalker-34381 | Restrict comments to members who posted first | https://www.reddit.com/r/ModSupport/comments/1u8dzd7/ | No |
| u/Gojo_dev | Cross-sub mod analytics | https://www.reddit.com/r/Devvit/comments/1pgzctl/ | No |
| u/steamwhistler | Modmail auto-reply | https://www.reddit.com/r/ModSupport/comments/1n1qnzk/ | No |
| u/coopersoar | Clear modqueue posts from suspended accounts (**row 1**) | https://www.reddit.com/r/modhelp/comments/1q8k7dv/ | No |
| u/pixiefarm | Reverse image search vs off-Reddit | https://www.reddit.com/r/modhelp/comments/1tjvka3/ | No |
| u/Baconkings | Auto-summarize thread to pinned comment | https://www.reddit.com/r/modhelp/comments/1shy443/ | No |
| u/average_sk_player | Auto-spoiler tagging | https://www.reddit.com/r/ModSupport/comments/1n5kj9a/ | No |
| u/SuMianAi | Block a whole sentence | https://www.reddit.com/r/ModSupport/comments/1q6egp5/ | No |
| u/royal_rose_ | Link enrichment | https://www.reddit.com/r/modhelp/comments/1qywvrh/ | No |
| u/WombatHat42 | New-account verification | https://www.reddit.com/r/ModSupport/comments/1tutqbo/ | No |

One sweep-B thread is recent enough to be worth a reply: u/RodneyOgg, 2025-07-18,
asking how r/TipOfMyTongue removes posts when OP doesn't engage — **row 1**, and the
only B author still plausibly active.
https://www.reddit.com/r/AutoModerator/comments/1m35fbq/

u/flattenedbricks is not a prospect — he is the incumbent.

---

## Query performance across both sweeps

| Query | A (5 subs, year) | B (AutoMod, all) | Verdict |
|---|---|---|---|
| `automod can't` | 0 | **19** | Best single query in the instrument — needs `time=all` |
| `automoderator can't` | 0 | 5 | Same; 2 of 5 were false positives |
| `is there a bot that` | 5 | 4 | Reliable in both windows |
| `is there a tool` | 5 | 1 | Best recent-demand query |
| `any way to automatically` | 3 | 5 | Solid in both |
| `is there an app that` | 2 | 0 | Low volume, high precision |
| `spending hours` | 6 | 0 | **Worst** — 5 of 6 were burnout essays and mod-recruitment ads |
| `wish there was` | 1 | 1 | Both false positives |
| `how do you all handle` | 1 | 0 | Thin |
| `we do this manually` | 0 | 0 | **Never fired. Retire or rewrite it.** |

`we do this manually` has now returned zero across 60 searches. Drop it.
