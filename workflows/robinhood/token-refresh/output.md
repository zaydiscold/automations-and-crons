# Output format

Exactly four lines. The attached model may reason about the auth path, but it does not get to improvise the receipt.

```text
As of: YYYY-MM-DD HH:MM:SS PT
🔑 Robinhood auth · refreshed + verified 🌸
Verification: N accounts · source: CDP|LevelDB|existing token
runtime: <actual provider> · <actual model> · reasoning=<actual effort>
```

Degraded and failed runs replace lines 2–3 with the exact concise reason. Nothing follows the runtime line.
