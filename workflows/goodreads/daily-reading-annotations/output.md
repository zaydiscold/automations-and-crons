# Output format

Deterministic script output; no model rewrites it.

## No new content

```text
📚 **Goodreads · Mon Aug 24, 4:01 AM PT**

**Currently reading — N**
• <every current title, one per line>

• Highlights/notes: 0
• Published: yes — N/N books
🌸
```

## Highlights and/or notes found

```text
📚 **Goodreads · Mon Aug 24, 4:01 AM PT**

**Currently reading — N**
• <every current title, one per line>

• Highlights: Book A +N · Book B +N
• Notes: Book A +N · Book C +N
• Published: yes — N/N books
🌸
```

If either highlights or notes has activity, always split them into two lines and show `0` for the inactive type. “Notes” means written text attached to a highlight. Goodreads social comments are a separate feature and are excluded.
