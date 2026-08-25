# Security

Do not commit scheduler IDs, delivery/chat IDs, account numbers, balances, order IDs, wallet addresses, tax lots, cookies, CSRF values, tokens, webhook URLs, API keys, personal machine paths, private hostnames/IPs, or raw private receipts.

The public output templates use placeholders. The actual jobs keep private values in their local state and delivery channels.

Run `python scripts/validate.py` plus a secret scanner before every push. Report accidental exposure privately; do not paste the secret into a public issue.
