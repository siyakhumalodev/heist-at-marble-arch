---
applyTo: "**/*.py"
description: "Vault security rules for Python files in the Heist at Marble Arch repo"
---

# Vault security rules for Python

- Never hard-code a vault code, a passphrase, or anything shaped like a vault code (for example `WORD-1234`). Read them with `os.environ`, through `vault_logic.load_config()` where possible.
- Agent instructions at Level 3 must not include the code or passphrases. Add or keep a unit test that asserts this (see `tests/test_vault_logic.py`).
- Check passphrases with `hmac.compare_digest` on normalised values. Evaluate every comparison, without short-circuiting.
- Attempt limits and lockouts live in code and are thread-safe (`threading.Lock`).
- Tools return plain strings that start with a status word (`OPENED`, `DENIED`, `LOCKED`) so the model can't misread them.
- Reports, logs and issue comments mask codes (see `heist/vault_client.redact`).
