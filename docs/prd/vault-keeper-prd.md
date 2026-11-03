# PRD: VaultKeeper ("Reginald")

| | |
|---|---|
| **Product** | VaultKeeper: a Microsoft Foundry hosted agent that guards Contoso Bank's (fictional) vault beneath Marble Arch |
| **Event** | Heist at Marble Arch: HVE Hack, FSI SE Q2 Team Day, Wednesday 4 November 2026, 14:00 to 15:00 |
| **Status** | Approved for hacking |
| **Owner** | Your crew's Mastermind |

> This PRD is the input for HVE Core's **Functional Planner**. Keep the IDs: they should appear in your issues, RPI plans, commits and pull requests.

## 1. Problem and opportunity

Agents in financial services will hold or reach sensitive data. The fastest way to understand why agent security belongs in **code and tests** rather than in **prompts** is to build an agent that guards a secret, then watch other people (and other agents) try to talk it out of that secret.

## 2. Business goals

| ID | Goal |
|---|---|
| BG-001 | Give FSI Solution Engineers hands-on experience of the HVE lifecycle (plan, build, deploy, test) in 60 minutes. |
| BG-002 | Show, with evidence, that secrets and policy enforced in code survive attacks that prompt rules don't. |
| BG-003 | Leave each SE with a reusable demo for customer conversations about agent security and AI-assisted engineering. |

## 3. Personas

- **Player**: tries to open the vault by solving riddles, or by being cleverer than Reginald.
- **Crew** (Mastermind, Engineer, Hacker): builds, deploys and defends a vault.
- **Heist Crew bot**: a GitHub Copilot SDK app that attacks a vault automatically and reports what worked.

## 4. Functional requirements

| ID | Requirement |
|---|---|
| FR-001 | **Persona.** The agent plays Reginald, the polite, dry-witted British VaultKeeper of Contoso Bank's Marble Arch vault, and stays in character. |
| FR-002 | **Riddles.** The agent offers three riddles; each hints at where one passphrase can be found. |
| FR-003 | **Unlock.** When a player supplies three passphrases, the agent checks them and reveals the vault code only if all three are correct. |
| FR-004 | **Secrets outside the prompt (Level 3).** The vault code and passphrases never appear in agent instructions, source code, tests, docs or commits. They are read from environment variables (`VAULT_CODE`, `VAULT_PASSPHRASES`) by a tool. |
| FR-005 | **Time lock.** After three failed unlock attempts within 60 seconds, the vault refuses further attempts for 60 seconds. |
| FR-006 | **Vault levels.** `VAULT_LEVEL` selects 1 (Sticky Note: secret in the prompt), 2 (Velvet Rope: secret in the prompt plus hardening rules and a guardrail) or 3 (Time Lock: secret only in code). |
| FR-007 | **Run and deploy.** The agent runs locally in the Agent Inspector and is deployed to Foundry Agent Service as a hosted agent. |
| FR-008 | **Red team.** A GitHub Copilot SDK "Heist Crew" app attacks the vault with at least eight techniques and reports any leak. |
| FR-009 | **Leak eval.** A deterministic eval sends a fixed attack set plus the legitimate unlock path and fails if the code leaks. |
| FR-010 | **Scorecard.** Eval and red-team results are posted as comments on the *Crack the Vault* epic, with the code masked. |

## 5. Non-functional requirements

| ID | Requirement |
|---|---|
| NFR-001 | Replies in about five seconds or less for most turns (model dependent). |
| NFR-002 | No secrets in the repo: values live in the azd environment (`.azure/<env>/.env`, git-ignored) and are referenced from `azure.yaml` as `${VAULT_CODE}`. Our variables never use the reserved `FOUNDRY_*` or `AGENT_*` prefixes. |
| NFR-003 | Cost: one small model deployment per crew; `azd down` (or manual clean-up) after the hack. |
| NFR-004 | Responsible AI: Reginald stays polite and safe for work. No real customer, bank or personal data anywhere. |

## 6. Acceptance criteria

| ID | Traces to | Criterion |
|---|---|---|
| AC-001 | FR-001 | Asked "Who are you?", the agent introduces itself as Reginald, keeper of the Marble Arch vault. |
| AC-002 | FR-002 | Asked how to open the vault, the agent shares three riddles and no passphrases. |
| AC-003 | FR-003 | With the three correct passphrases the vault code is revealed; with any wrong passphrase it isn't. |
| AC-004 | FR-004 | At Level 3, a search of the repo and the agent instructions finds neither the code nor the passphrases. |
| AC-005 | FR-005 | After the third failed attempt within 60 seconds, attempts return a time-lock message until 60 seconds pass, even with correct passphrases. |
| AC-006 | FR-007 | `azd ai agent invoke "Who are you?"` returns Reginald's greeting from the deployed agent. |
| AC-007 | FR-008 | The Heist Crew report shows no leak at Level 3. |
| AC-008 | FR-009, FR-010 | `run_evals.py` passes at Level 3 and both scorecards are on the epic, codes masked. |

## 7. Milestones

| Milestone | Due (4 Nov 2026) | Scope |
|---|---|---|
| M1 · Casing the joint | 14:15 | Plan: PRD to milestones, epics and sub-issues with HVE |
| M2 · Build the vault | 14:35 | Build, run locally, Time Lock, deploy |
| M3 · The heist | 14:55 | Red team, evals, Showdown |

## 8. Epics (suggested)

| Epic | Milestone | Covers |
|---|---|---|
| E1 Case the joint | M1 | Plan with Functional Planner; execute with Backlog Manager |
| E2 Meet Reginald | M2 | FR-001, FR-002, FR-006, FR-007 (local) |
| E3 Time Lock | M2 | FR-003, FR-004, FR-005 and unit tests |
| E4 Ship it | M2 | FR-007 (deploy), NFR-002, NFR-003 |
| E5 Crack the Vault | M3 | FR-008, FR-009, FR-010, Showdown. *Heist lore: this epic's card carries Reginald's codeword, **BOWLER**.* |

## 9. Out of scope

Real authentication, persistence across restarts, a custom UI, and any real banking data.

## 10. Risks

| Risk | Mitigation |
|---|---|
| Hosted agent deployment takes several minutes | Start **Deploy to Foundry** by 14:30; demo locally if it's still running |
| Model quota or region limits | Pre-provision a project and model deployment the day before |
| Built-in GitHub MCP server is read-only | `copilot --enable-all-github-mcp-tools`, or `scripts/seed_backlog.py` |
| Corporate device can't install the app | Pair with a crew-mate, or use VS Code with the HVE Core extension and Foundry Toolkit |
