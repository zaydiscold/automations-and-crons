# Output format

There is no model. The script emits transition alerts and a separate private heartbeat.

```text
✅ Cron roster healthy: <checked contracts>
```

```text
🚨 Cron roster BROKEN: <job>: <exact violated contract>
```

No-change ticks are silent on the chat delivery path. That is why a separate heartbeat must watch the watcher.
