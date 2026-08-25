# Automations and Crons

I'm uploading the cron jobs and automations I actually use as a checkpoint and for transparency. Some are plain scripts. Some run through Hermes with no agent. Some spin up an agent and a model because the output needs judgment instead of a fixed template.

This is not a starter kit or a one-click install. It is the shape of the jobs, the schedules, the runtime choices, the output contracts, and the parts that still depend on private code or local setup.

Obviously I removed keys, account IDs, chat IDs, machine paths, balances, and raw private output.

## What's here

| Automation | Cadence | Scheduler/runtime | Model attached? | Output |
|---|---:|---|---|---|
| [Goodreads reading + annotations](workflows/goodreads/daily-reading-annotations/) | daily | script / no-agent; Hermes wrapper optional | no | [exact Telegram format](workflows/goodreads/daily-reading-annotations/output.md) |
| [Robinhood token refresh](workflows/robinhood/token-refresh/) | every few days | Hermes agent | yes — Luna Max + inherited fallbacks | [exact four-line receipt](workflows/robinhood/token-refresh/output.md) |
| [Robinhood premarket brief](workflows/robinhood/premarket-brief/) | weekdays | Hermes agent | yes — Luna Max + inherited fallbacks | [exact report template](workflows/robinhood/premarket-brief/output.md) |
| [Robinhood midday snapshot](workflows/robinhood/midday-snapshot/) | weekdays | Hermes agent | yes — Luna Max + inherited fallbacks | [exact report template](workflows/robinhood/midday-snapshot/output.md) |
| [Robinhood postmarket summary](workflows/robinhood/postmarket-summary/) | weekdays | Hermes agent | yes — Luna Max + inherited fallbacks | [exact report template](workflows/robinhood/postmarket-summary/output.md) |
| [Obsidian parity-first sync](workflows/obsidian/parity-first-sync/) | paused | script / no-agent | no | [paused output contract](workflows/obsidian/parity-first-sync/output.md) |
| [Cron roster guard](workflows/monitoring/roster-guard/) | every five minutes | script / no-agent | no | [transition alerts](workflows/monitoring/roster-guard/output.md) |

[`matrix.csv`](matrix.csv) is the quick machine-readable view.

## The runtime labels actually mean something

Every `job.json` says:

- what scheduler currently runs it;
- whether it is a plain script, a no-agent job, or a model-backed agent job;
- whether a model is attached;
- the provider, model, reasoning level, and inherited fallback chain when there is one;
- what other schedulers could run it after adapting the private dependencies;
- the exact output template;
- why copying the folder is not enough.

Hermes is one runner used here, not the identity of the repo. The script jobs can run under Task Scheduler, system cron, launchd, or another runner once paths and local dependencies are adapted. The agent jobs need Hermes or another tool-capable agent runner.

## Copying one of these

Copying a folder does **not** make the automation work.

1. Read `job.json`, especially `runtime`, `copying`, and `limitations`.
2. Read `output.md`; it is part of the contract, not decoration.
3. Replace the private client/script/session/storage pieces with your own.
4. Decide whether you actually need a model. If the output is deterministic, use a script.
5. Create the schedule in whatever runner you use.
6. Run it manually and verify the real source or state change. Scheduler `ok` is not proof.
7. Add a heartbeat if the normal path can be silent.

The brokerage folders are not trading software. The Goodreads folder does not include a session or the private collector. The Obsidian folder should remain paused until independent trees have backups and a reviewed merge plan.

## Layout

```text
workflows/<domain>/<automation>/
  job.json      schedule, runtime/model, dependencies, checks, limitations
  prompt.md     what the agent/script is supposed to do when useful
  output.md     exact output format or the honest current boundary
schema/job.schema.json
scripts/validate.py
matrix.csv
```

## Checks

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

## Reuse

There is no open-source license attached to this repository. The code and writing remain all rights reserved. Reading it or borrowing the general ideas is fine; do not assume permission to redistribute substantial copies of the repository.
