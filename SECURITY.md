# Security policy

## Never publish

- scheduler/job IDs or delivery/chat IDs;
- account numbers, portfolio values, order IDs, wallet addresses, or tax lots;
- cookies, CSRF values, bearer tokens, refresh tokens, webhook URLs, or API keys;
- personal filesystem paths, private hostnames/IPs, or raw cron output;
- raw Goodreads highlights/comments or private Obsidian content.

Use placeholders and bounded metadata only. Run `python scripts/validate.py` and a secret scanner before every push.

Report accidental exposure privately to the repository owner. Do not open a public issue containing the secret.
