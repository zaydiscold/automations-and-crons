# Hermes Cron Playbooks

A public, sanitized look at how a small personal-operations stack uses [Hermes Agent](https://hermes-agent.nousresearch.com/docs) cron jobs for books, brokerage reporting, backup safety, and monitoring.

This repository publishes the **operating contracts**, not a raw scheduler database. It contains no live job IDs, chat IDs, account identifiers, machine paths, cookies, tokens, portfolio values, or private prompts.

## Why this exists

A useful cron is more than a schedule. Every workflow here declares:

- what wakes it up;
- which source is authoritative;
- whether it reads or mutates state;
- exactly how success is verified;
- what receipt is retained and delivered;
- how it fails loudly without inventing success.

## Workflow map

| Domain | Workflow | Cadence | Runtime | Risk |
|---|---|---:|---|---|
| Goodreads | [daily reading + annotations](workflows/goodreads/daily-reading-annotations/) | daily | deterministic script | account write, narrowly scoped |
| Robinhood | [token refresh](workflows/robinhood/token-refresh/) | every few days | agent | auth state only |
| Robinhood | [premarket brief](workflows/robinhood/premarket-brief/) | weekdays | agent | read-only |
| Robinhood | [midday snapshot](workflows/robinhood/midday-snapshot/) | weekdays | agent | read-only |
| Robinhood | [postmarket summary](workflows/robinhood/postmarket-summary/) | weekdays | agent | read-only |
| Obsidian | [parity-first sync](workflows/obsidian/parity-first-sync/) | paused by default | deterministic script | filesystem write |
| Monitoring | [roster guard](workflows/monitoring/roster-guard/) | every five minutes | deterministic script | monitoring write |

The machine-readable cross-workflow view is [`matrix.csv`](matrix.csv).

## Structure

```text
workflows/<domain>/<workflow>/
  job.json      public operating contract
  prompt.md     sanitized prompt/script behavior where useful
schema/job.schema.json
scripts/validate.py
matrix.csv
```

## Safety boundary

Do **not** export `jobs.json` into this repository. Real scheduler state commonly contains stable IDs, delivery targets, local paths, account context, and operational instructions that should remain private.

The validator rejects common leaks and requires every mutating workflow to declare an approval boundary and read-back verification.

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

## Copying a playbook

1. Copy one workflow folder.
2. Replace every placeholder locally.
3. Create the cron with `hermes cron create` or the Hermes UI.
4. Run it manually once.
5. Verify the real source and retained receipt—not merely scheduler status `ok`.
6. Add an overdue/semantic monitor appropriate to the schedule.

## Honest limitations

- These are patterns from one real homelab, not universal defaults.
- Brokerage jobs are reporting examples, not investment advice.
- The Goodreads workflow intentionally publishes only annotations that the account owner pre-authorized for public visibility.
- The Obsidian workflow is paused until independent trees have been backed up and proven equivalent. Sync tools are not merge proofs.

## License

MIT. See [LICENSE](LICENSE).
