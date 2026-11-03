# 🧯 Break glass: the reference VaultKeeper

A complete Level 1 to 3 vault you can drop into any hosted-agent scaffold that uses
**Python + Microsoft Agent Framework + the Responses protocol** (what Microsoft Foundry Canvas
and `azd ai agent init` generate for the Basic or Hello world sample).

| File | What it does |
|---|---|
| `main.py` | Agent Framework agent served by `ResponsesHostServer` on port 8088. Level 3 adds the `get_riddles` and `try_unlock` tools. |
| `vault_logic.py` | Deterministic logic: config from `VAULT_*` variables, passphrase checks with `hmac.compare_digest`, three-attempt time lock, per-level instructions. Unit-tested in `tests/`. |

## Use it in 3 minutes

1. Find the folder with the scaffold's `main.py` (usually `src/<agent-name>/`). Copy **both** files over it.
   The scaffold's dependency files already cover every import, so you don't add packages.
2. Set your secrets in the azd environment (git-ignored):
   ```bash
   azd env set VAULT_LEVEL 3
   azd env set VAULT_CODE CREWNAME-1234
   azd env set VAULT_PASSPHRASES "word1,word2,word3"
   azd env set VAULT_RIDDLES "hint one||hint two||hint three"   # optional
   ```
3. Add them to the agent service's `env` map in `azure.yaml` (keep everything the scaffold generated; some versions call the map `environmentVariables`):
   ```yaml
   services:
     vault-keeper:
       host: azure.ai.agent
       # ...generated settings...
       env:
         PYTHONNOUSERSITE: "1"
         VAULT_LEVEL: ${VAULT_LEVEL}
         VAULT_CODE: ${VAULT_CODE}
         VAULT_PASSPHRASES: ${VAULT_PASSPHRASES}
         VAULT_RIDDLES: ${VAULT_RIDDLES}
   ```
   Don't add `FOUNDRY_PROJECT_ENDPOINT`: the platform injects it, and `azd ai agent run` sets it locally. `FOUNDRY_*` and `AGENT_*` are reserved.
4. **Inspect Locally** (or `azd ai agent run`), then **Deploy to Foundry** (or `azd deploy`).
5. `azd ai agent invoke "Who are you?"`, then `azd ai agent invoke "How do I open the vault?"`

## Flip levels live (the demo moment)
```bash
azd env set VAULT_LEVEL 1 && azd ai agent run      # Sticky Note: crack it with heist_crew.py
azd env set VAULT_LEVEL 3 && azd ai agent run      # Time Lock: same attacks, vault holds
```
Restart the local agent after each change; redeploy with `azd deploy` for the hosted version.

## Model deployment name
`main.py` reads `AZURE_AI_MODEL_DEPLOYMENT_NAME` (the variable the Foundry samples use). If your scaffold uses another name, map it in `azure.yaml`.
