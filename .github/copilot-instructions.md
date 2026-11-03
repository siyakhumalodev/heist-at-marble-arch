# Copilot instructions: Heist at Marble Arch

This repository is a 60-minute hack. Optimise for working software, small diffs and clear tests.

## Product
- We are building **VaultKeeper ("Reginald")**, a Microsoft Foundry **hosted agent**: Python 3.13, Microsoft Agent Framework, Responses protocol, code deployment with `azd`.
- Requirements: `docs/prd/vault-keeper-prd.md` (IDs BG-, FR-, NFR-, AC-). Cite IDs in plans, commits and pull requests.
- Backlog: GitHub Issues with milestones M1 to M3, epics as parent issues and stories as sub-issues.
- Break-glass reference implementation: `src/vault-keeper/` (`main.py`, `vault_logic.py`).

## Security rules (non-negotiable, FR-004 and NFR-002)
- Never write the vault code or passphrases into source, agent instructions, tests, docs, issues or commit messages.
- Read secrets from environment variables (`VAULT_CODE`, `VAULT_PASSPHRASES`, `VAULT_LEVEL`, `VAULT_RIDDLES`) set with `azd env set`, and reference them in `azure.yaml` as `${VAULT_CODE}`.
- Never use the reserved `FOUNDRY_*` or `AGENT_*` prefixes for our own variables, and don't declare `FOUNDRY_PROJECT_ENDPOINT` in `azure.yaml`.
- At Level 3 the model must never see the secrets: only the `try_unlock` tool checks passphrases and releases the code.
- Compare secrets with `hmac.compare_digest`. Enforce attempt limits and lockouts in code, not in the prompt.

## Engineering conventions
- Keep deterministic logic in plain Python (like `vault_logic.py`) and cover it with pytest (`pytest tests/`).
- Agent tools: small, typed with `Annotated[..., Field(description=...)]`, decorated with `@tool(approval_mode="never_require")`; the docstring says when to call the tool.
- Keep the scaffold that Microsoft Foundry Canvas or `azd ai agent init` generated; don't hand-edit generated infrastructure unless asked.
- Test locally with **Inspect Locally** or `azd ai agent run` before **Deploy to Foundry** or `azd deploy`.
- After any change to instructions or tools, run `heist/run_evals.py` and `heist/heist_crew.py` (see the `heist-red-team` skill).
