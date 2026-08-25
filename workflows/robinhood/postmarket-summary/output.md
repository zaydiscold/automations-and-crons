# Output format

````text
As of: YYYY-MM-DD HH:MM:SS PT

**Post-Market Summary — Weekday Mon DD**

```text
total_equity:  $X
day_pnl:       ±$Y
after_hours:   ±$Z
```

**Per account**
```text
<Account>          $X    day ±$Y    AH ±$Z
```

**Top $ movers**
- **SYMBOL** ±$X — live-supported explanation

**Options / positioning**
- Up to four material bullets.

**Tomorrow**
One verified event/risk line.

`✓ Snapshot: postmarket · N options · 0 errors`
🌸
runtime: <actual provider> · <actual model> · reasoning=<actual effort>
````

Maximum 2,700 characters / 38 nonblank lines before the runtime footer. Nothing follows runtime.
