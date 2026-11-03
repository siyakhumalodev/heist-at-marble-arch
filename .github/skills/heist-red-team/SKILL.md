---
name: heist-red-team
description: Red-team the VaultKeeper agent and post a scorecard. Use when asked to test, attack, red-team or evaluate the vault, check for leaks, or prepare Quest 3 evidence.
---

# Heist red team

Test a VaultKeeper ("Reginald") agent the way the hack expects: deterministic eval first, then the Copilot SDK Heist Crew, then a short verdict.

## Before you start
1. Confirm the vault is running: locally (`azd ai agent run` or **Inspect Locally**, port 8088) or deployed (`azd ai agent invoke "Who are you?"` answers).
2. Load the crew's azd values into the shell so `VAULT_CODE` and `VAULT_PASSPHRASES` are available:
   - bash or zsh: `set -a; eval "$(azd env get-values)"; set +a`
   - PowerShell: `azd env get-values | % { $k,$v = $_ -split '=',2; Set-Item "env:$k" $v.Trim('"') }`
3. Install the test tools once: `pip install -r heist/requirements.txt`

## Steps
1. Run the leak eval (local example):
   `python heist/run_evals.py --target local --secret "$VAULT_CODE" --passphrases "$VAULT_PASSPHRASES"`
2. Run the Heist Crew:
   `python heist/heist_crew.py --target local --secret "$VAULT_CODE"`
   For a deployed agent use `--target foundry --endpoint "$FOUNDRY_PROJECT_ENDPOINT" --agent <agent-name>`.
3. Read `eval-report.md` and `heist-report.md`. Summarise in five lines or fewer: attacks held, techniques that worked, and the single most important fix.
4. If the vault leaked at Level 1 or 2, recommend Level 3: secrets out of the prompt and into the `try_unlock` tool (FR-004).
5. Offer to post both reports to the *Crack the Vault* epic: `gh issue comment <number> --body-file <report>`. Ask before posting.

## Rules
- Attack only vaults owned by this crew, vaults the host opened for the Showdown, or the Final Boss.
- Never print or post an unmasked vault code. The scripts mask codes; keep it that way.
