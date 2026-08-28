# Output format

This one is deterministic. No model is attached and the script prints the final Telegram Markdown itself.

```text
📚 **Goodreads · Mon Aug 24, 4:01 AM PT**

**Reading now — N**
• <every current title, one per line, verbatim>

**Annotations**
• <exact new Goodreads-visible highlight/note delta, or an explicit no-visible-change statement>
• Publish sweep: N/N books accepted + verified
• ⚠️ <sync-pending warning only when a user-reported action remains absent after the sweep>

**Review comments — separate from Kindle highlights**
• N current · <+N new review comments | no new review comments>
🌸
```

Never translate “not visible in Goodreads” into “the user made zero highlights.”
