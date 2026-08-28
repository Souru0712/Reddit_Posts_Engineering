# Devvit Recon — Week 1 capture harness

`recon.py` runs the instrument's 10 exact search queries across the 5 recon
subreddits (50 searches), sorted **Top → Year**, and writes the capture sheet.

## Run it

Reddit app credentials — https://www.reddit.com/prefs/apps, type **script**:

```bash
pip install praw==7.7.1
export REDDIT_CLIENT_ID=...
export REDDIT_CLIENT_SECRET=...
python recon.py
```

Credentials also resolve from `config/config.conf` `[api_keys]` if the env vars
are unset. The harness is **read-only** (client-credentials OAuth) — it needs no
account password and cannot write to Reddit.

Takes about a minute. Outputs:

| File | Contents |
|---|---|
| `data/output/recon_capture.md` | Hit grid, capture table, distribution-plan prospect list |
| `data/output/recon_corpus.json` | Full records incl. post bodies — the input for chore clustering |

## Flags

```bash
python recon.py --sort new              # the instrument's second pass
python recon.py --no-quote              # loose terms instead of exact phrase
python recon.py --time all              # widen beyond the year
python recon.py --limit 250             # more hits per query
python recon.py --subreddits AutoModerator ModSupport
python recon.py --queryset chore                # 10 chore-noun queries
python recon.py --queryset both                 # all 20
```

The default `tool` query set contains no chore nouns — no "modmail", "flair",
"queue", "sticky" — so it can only surface demand phrased as a generic tool
request. `--queryset chore` tests for demand that set structurally cannot see.
Run it before treating any frequency-of-1 row as settled.

Default is `--sort top --time year` with phrase-quoted queries. Quoting is what
makes these *exact* queries: `"automod can't"` matches the phrase, unquoted
matches the words anywhere. Run `--no-quote` as a second sweep if the phrase
pass comes back thin.

## What the harness does and does not decide

It collects and dedupes threads. It does **not** cluster them into distinct
chores — that is the reading work, and `Times seen` in the generated table is
*how many queries surfaced that thread*, not how often the chore recurs.

Chore-level frequency comes from collapsing rows that say the same thing. Feed
`recon_corpus.json` back into a session to do that clustering, then score.
