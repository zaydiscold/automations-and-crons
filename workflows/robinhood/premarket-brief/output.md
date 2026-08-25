# Output format

````text
As of: YYYY-MM-DD HH:MM:SS PT

# Robinhood Premarket — Weekday Mon DD
_Baseline: prior close → current premarket move_

---

### Portfolio Overview — $TOTAL
```text
Account             Equity      Overnight
<Account>           $X          ±$Y
```
**Portfolio theta:** -$X/day | **Overnight:** ±$Y

---

### ⚠️ Critical Alerts
1. **Alert title** — concise, live-supported explanation

### Biggest Dollar Drivers
| Symbol | Move | Why |
|---|---:|---|
| X | ±$Y | live-supported reason |

### Options / Expiration Watch
- Up to three material contracts

### Today
One grounded setup paragraph.

**Bottom line:** one sentence.

`✓ Snapshot: premarket · N options · 0 errors`
🌸
runtime: <actual provider> · <actual model> · reasoning=<actual effort>
````

Maximum 3,600 characters / 52 nonblank lines before the runtime footer. Nothing follows runtime.
