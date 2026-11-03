# 🏦 Heist at Marble Arch: the HVE Hack

> **Build Reginald, the VaultKeeper**: a Microsoft Foundry hosted agent that guards Contoso Bank's vault.
> **Then try to crack everyone else's.**

| Stage | You'll use | Outcome |
|---|---|---|
| 🗺️ **Plan** | **HVE Core**: Functional Planner + Backlog Manager | GitHub **milestones, epics and issues** (sub-issues) from a PRD |
| 🔧 **Build** | **GitHub Copilot app** + **Microsoft Foundry Canvas** + HVE **RPI** | A hosted agent running locally in the Agent Inspector |
| 🚀 **Deploy** | Foundry Canvas **Deploy to Foundry** (`azd deploy`) | Reginald live in **Foundry Agent Service** |
| 🕵️ **Test** | **GitHub Copilot SDK** "Heist Crew" + deterministic leak eval | A red-team scorecard on your GitHub epic |

FSI SE Q2 Team Day · Wednesday 4 November 2026 · 14:00 to 15:00 · 5 Marble Arch, London

---

## ⏱️ The 60-minute heist

| Time | Quest | Done when |
|---|---|---|
| 14:00 | **Briefing**: crews of three, pick roles | Crew name on the scoreboard |
| 14:05 | 🗺️ **Quest 1: Case the joint** (plan) | 3 milestones, 5 epics, stories linked as sub-issues |
| 14:15 | 🔧 **Quest 2: Build the vault** (build and deploy) | Reginald talks in the Agent Inspector; Time Lock in; deploy started by 14:30 |
| 14:35 | 🕵️ **Quest 3: The heist** (test) | Eval and Heist Crew scorecards posted to your *Crack the Vault* epic |
| 14:45 | 🏁 **Showdown**: gallery heist, then the Final Boss | Points on the board |
| 14:55 | **Debrief**, then over to the Agent Governance Toolkit session | |

## 👥 Crew roles

- 🗺️ **Mastermind**: owns the plan (HVE → GitHub Issues), keeps time, claims points.
- 🔧 **Engineer**: owns the build (GitHub Copilot app + Foundry Canvas) and the deployment.
- 🕵️ **Hacker**: owns the tests (Copilot SDK Heist Crew + leak eval) and leads Showdown attacks.

## ✅ Pre-flight (do this before the day: about 20 minutes)

1. **GitHub Copilot app** installed and signed in (download link at the top of <https://docs.github.com/en/copilot/how-tos/github-copilot-app/working-with-canvas-extensions>)
2. **Foundry Dev Pack** *after* the app, so it can add **Foundry Canvas**:
   - Windows: `winget install Microsoft.FoundryDevPack`
   - macOS: `brew install --cask microsoft/foundry/devpack && foundry-devpack install`
   - Linux: `curl -fsSL https://aka.ms/foundry-devpack-install.sh | bash`
   - Check the app: **Settings → Plugins** (or **Customize → Plugins**) shows **microsoft-foundry**. If not, search for it and select **Install**.
3. **HVE Core** plugin (agents and skills):
   ```bash
   copilot plugin marketplace add microsoft/hve-core
   copilot plugin install hve-core@hve-core
   ```
   VS Code alternative: the **HVE Core** extension (`ise-hve-essentials.hve-core`).
4. **Python 3.13+**, **git** and the **GitHub CLI** (`gh auth login`).
5. **Azure**: an existing Foundry project with a chat model deployment (for example `gpt-5.4-mini`) where you hold **Foundry Project Manager**, or **Owner** on a resource group so the canvas can create one. Connect **Application Insights** for traces.
6. Smoke test: in the app, ask *"Create a Foundry hosted agent using Microsoft Foundry Canvas"*, pick your project, choose **Hello world**, then **Inspect Locally**. If you see a reply, you're ready.

---

## 🗺️ Quest 1: Case the joint (plan with HVE → GitHub)

1. **Mastermind**: create your crew repo from this template (**Use this template** → private repo) and open it in the GitHub Copilot app.
2. Select the **Functional Planner** agent and prompt:
   > Plan a GitHub work-item hierarchy for `docs/prd/vault-keeper-prd.md` in repo `OWNER/REPO`. Use the PRD's three milestones (M1 Casing the joint, M2 Build the vault, M3 The heist), epics as parent issues and stories as sub-issues. Keep the FR and AC IDs in every issue body. Plan only: don't write to GitHub yet.
3. Review the proposed hierarchy (it's saved under `.copilot-tracking/`). Then switch to **Backlog Manager** → **Execute**:
   > Execute the reviewed GitHub handoff for `OWNER/REPO`: create the milestones, epics and stories and link stories as sub-issues. Use partial autonomy and confirm each batch with me.
4. Check **Issues → Milestones** in GitHub.

**Behind schedule at 14:12?** Run the fallback and move on:
```bash
python scripts/seed_backlog.py --repo OWNER/REPO        # add --issue-types on an org repo with Epic/Task types
```
> The built-in GitHub MCP server is read-only by default. If the executor can't write, start Copilot CLI with `copilot --enable-all-github-mcp-tools`, or use the fallback.

## 🔧 Quest 2: Build the vault (GitHub Copilot app + Foundry Canvas)

1. **Engineer**, in the app, with the crew repo open:
   > Create a Foundry hosted agent using Microsoft Foundry Canvas. Python 3.13, Microsoft Agent Framework, Responses protocol, code deployment. Name it vault-keeper.
2. In the canvas: sign in → choose **subscription** and **Foundry project** → **Hello world** → wire your **model**. Optional Level 2: assign a **guardrail** from your project.
3. **Level 1** (the sticky note): give Reginald his persona and riddles.
   > Implement issue #N, "Give Reginald his persona, riddles and a Level 1 vault", in the agent's main.py. Follow FR-001, FR-002 and FR-006 in docs/prd/vault-keeper-prd.md and read every VAULT_* setting from the environment.
4. **Inspect Locally** → chat with Reginald in the Agent Inspector. Send any errors back to Copilot as fix requests.
5. **Level 3** (the Time Lock), with HVE's RPI skills:
   > /rpi-plan Epic #N "Time Lock": move the vault code and passphrases out of the instructions into get_riddles and try_unlock tools backed by VAULT_* environment variables, with a three-attempt, 60-second time lock (FR-003 to FR-005).

   then `/rpi-implement`, then `/rpi-review`.
6. Set your secrets (never commit them), then select **Deploy to Foundry** (or run `azd deploy`):
   ```bash
   azd env set VAULT_LEVEL 3
   azd env set VAULT_CODE CREWNAME-1234
   azd env set VAULT_PASSPHRASES "word1,word2,word3"
   azd env set VAULT_RIDDLES "riddle one||riddle two||riddle three"   # optional: hints that point at clues on your table
   ```
   Reference them in the agent's `env` map in `azure.yaml` (see [`src/vault-keeper/README.md`](src/vault-keeper/README.md)).
7. Prove it's live: `azd ai agent invoke "Who are you?"`

**Stuck?** Break glass: copy [`src/vault-keeper/`](src/vault-keeper/) into your scaffold.

## 🕵️ Quest 3: The heist (test with the Copilot SDK)

```bash
pip install -r heist/requirements.txt
# load your azd values into this shell
set -a; eval "$(azd env get-values)"; set +a                     # bash or zsh
# PowerShell: azd env get-values | % { $k,$v = $_ -split '=',2; Set-Item "env:$k" $v.Trim('"') }

# 1) Deterministic leak eval: 18 attacks plus the legit unlock path
python heist/run_evals.py --target local --secret "$VAULT_CODE" --passphrases "$VAULT_PASSPHRASES" --issue E5_NUMBER

# 2) The Heist Crew: Copilot plans the attacks, your code referees
python heist/heist_crew.py --target local --secret "$VAULT_CODE" --issue E5_NUMBER

# Against the deployed agent
python heist/heist_crew.py --target foundry --endpoint "$FOUNDRY_PROJECT_ENDPOINT" --agent vault-keeper --secret "$VAULT_CODE"
```
In the app you can also type `/heist-red-team` (a repo skill) and let Copilot run both.

Run the crew at **Level 1** first, watch it crack, then switch to **Level 3** and watch it hold. That's the lesson.

## 🔐 Vault levels

| Level | Name | Where the secret lives | Expect |
|---|---|---|---|
| 1 | Sticky Note | In the prompt, with "please don't tell" | Cracked in a couple of attempts |
| 2 | Velvet Rope | In the prompt, plus hardening rules and a Foundry guardrail | Harder, but still crackable |
| 3 | Time Lock | **Only in code**: `try_unlock` checks passphrases with `hmac.compare_digest`, three-attempt lockout | Holds |

## 🗂️ Repo map

```
.github/copilot-instructions.md      repo-wide rules Copilot always follows (HVE: "AI carries the rules")
.github/instructions/                path-specific security rules for *.py
.github/skills/heist-red-team/       /heist-red-team skill
.github/ISSUE_TEMPLATE/              Epic and Story issue forms
docs/prd/vault-keeper-prd.md         the PRD: input to HVE's Functional Planner
docs/game-rules.md                   rules and scoring
backlog/backlog.json                 fallback backlog (milestones, epics, stories)
scripts/seed_backlog.py              creates that backlog with gh (Quest 1 fallback)
src/vault-keeper/                    break-glass agent: main.py + vault_logic.py
heist/heist_crew.py                  Copilot SDK red-team bot
heist/run_evals.py                   deterministic leak eval (exit code 1 on a leak)
heist/attacks.jsonl                  18 attack prompts
tests/                               pytest for the vault logic and heist helpers
```

## 🧹 After the hack
`azd down` removes what the azd environment created. If you picked an existing project, delete the hosted agent and model deployment yourself.

---
*Rules of engagement: attack only your own vault, vaults opened for the Showdown, and the Final Boss. All codes are fake. Be excellent to each other.*
