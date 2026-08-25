# Output format

There is no model. The private script owns the output and the job is paused.

```text
🗂️ Obsidian sync · paused|verified|failed
Manifests: <count/status>
Backups: <count/status>
Parity: <exact status; never inferred from a sync exit code>
Action: <none|additive merge|sync>
🌸
```

The copied job should stay paused until its own manifests, backups, and merge plan exist.
