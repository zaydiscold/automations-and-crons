# Output format

````text
As of: YYYY-MM-DD HH:MM:SS PT

**Midday Portfolio Snapshot — Weekday Mon DD**

```text
total_equity:  $X
day_change:    ±$Y
```

**Per account**
```text
<Account>          $X    ±$Y
```

**biggest day drivers**
| Name | Day P&L | Why |
|---|---:|---|
| X | ±$Y | live-supported reason |

**buying power / margin**
One or two readable lines.

**options / orders**
- Up to three material bullets.

**market pulse**
One grounded paragraph.

`✓ Snapshot: midday · N options · 0 errors`
🌸
runtime: <actual provider> · <actual model> · reasoning=<actual effort>
````

Maximum 2,800 characters / 42 nonblank lines before the runtime footer. Nothing follows runtime.

All rendered sections are required. The drivers table may contain 1–5 real rows; when there are zero material drivers, replace the table with `No material day driver.` If no material option/order item exists, print `- No material option or open-order exception.` Never emit placeholder rows or silently drop a required heading.
