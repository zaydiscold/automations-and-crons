# Output format

````text
As of: YYYY-MM-DD HH:MM:SS PT

# Robinhood Premarket — Weekday Mon DD
_Baseline: current extended-hours mark → prior regular close_

---

### Portfolio Overview — $TOTAL
```text
Account             Equity      Ext-hours vs close
<Account>           $X          ±$Y
```
**Portfolio theta:** -$X/day | **Ext-hours vs prior close:** ±$Y

---

### ⚠️ Critical Alerts
1. **Alert title** — concise, live-supported explanation

### Largest Extended-Hours Marks
| Symbol | Portfolio $ | Quote vs close |
|---|---:|---:|
| X | ±$Y | ±Z% |

### Options / Expiration Watch
- Up to three material contracts

### Today
One grounded setup paragraph. Mention a catalyst only when a current source from this run verifies it.

**Bottom line:** one sentence.

`✓ Snapshot: premarket · N options · 0 errors`
🌸
runtime: <actual provider> · <actual model> · reasoning=<actual effort>
````

Maximum 3,600 characters / 52 nonblank lines before the runtime footer. Nothing follows runtime.

`Ext-hours vs prior close` is the marked change from the prior regular close to capture time. At 05:30 PT it can combine the preceding post-close after-hours move with the current premarket move; it is not an isolated overnight session. Do not put the prior regular-session day P&L in the premarket headline or add it to this number.

All rendered sections are required. If there are no critical alerts, print `No material alert.` under that heading instead of inventing one. If no material option/expiration item exists, print `- No material option or expiration exception.` The extended-hours table may contain 1–5 real rows sorted by absolute portfolio `afterHoursChangeUsd`; when there are zero material marks, replace the table with `No material extended-hours mark.` Never emit a placeholder row or a mandatory explanation column.
