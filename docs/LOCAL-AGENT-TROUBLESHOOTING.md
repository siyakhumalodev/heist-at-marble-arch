# Local Agent Troubleshooting (Foundry Canvas Inspect Locally)

This guide captures the fixes that worked while running the hosted agent locally from Foundry Canvas (**Inspect Locally**).

## Scope

Applies to this flow:

1. Create Hosted agent in Foundry Canvas (`Hello world` template).
2. Use **Inspect Locally**.
3. Run and chat with the local preview agent.

---

## 1) `uv.toml` parse errors (`system-certs` unknown field)

### Symptom

Inspect Locally terminal shows an error like:

`Failed to parse: uv.toml ... unknown field 'system-certs'`

### Cause

The installed `uv` version does not support that key yet.

### Fix

1. Update `uv`:
   ```powershell
   winget upgrade --id AstralSh.uv
   uv --version
   ```
2. If still needed, use a global `uv` config at:
   `C:\Users\<your-user>\AppData\Roaming\uv\uv.toml`
3. Use compatible settings (example in section 3).

---

## 2) TLS handshake failure downloading dependencies from PyPI

### Symptom

`uv sync` fails with:

`Failed to download ... pydantic-core ... HandshakeFailure`

### Cause

Corporate network policy/certificate trust blocks direct package download from public sources.

### Fix (recommended)

Point `uv` to your Azure Artifacts Python feed and authenticate with PAT.

---

## 3) Configure global `uv` to use Azure Artifacts + PAT

Create/edit:

`C:\Users\<your-user>\AppData\Roaming\uv\uv.toml`

```toml
native-tls = true

[[index]]
name = "private-registry"
url = "https://pkgs.dev.azure.com/sk-customers/_packaging/sk-customers-feed/pypi/simple/"
default = true
```

Set credentials (username can be any non-empty value for Azure Artifacts):

```powershell
setx UV_INDEX_PRIVATE_REGISTRY_USERNAME "anything"
setx UV_INDEX_PRIVATE_REGISTRY_PASSWORD "<YOUR_PAT>"
```

Restart the Copilot app after `setx`.

Check whether env vars are present (without printing secret values):

```powershell
if ([string]::IsNullOrEmpty([Environment]::GetEnvironmentVariable("UV_INDEX_PRIVATE_REGISTRY_PASSWORD","User"))) { "NOT SET at user level" } else { "SET at user level" }
if ([string]::IsNullOrEmpty([Environment]::GetEnvironmentVariable("UV_INDEX_PRIVATE_REGISTRY_USERNAME","User"))) { "NOT SET at user level" } else { "SET at user level" }
```

---

## 4) `uv.lock` needs update / lockfile mismatch

### Symptom

`The lockfile at uv.lock needs to be updated, but --locked was provided`

### Cause

The lockfile is out of date relative to the generated project files.

### Fix

Run `uv lock` in the folder that contains `pyproject.toml` (for this scaffold, under `src/...`):

```powershell
cd C:\Users\<your-user>\.copilot\chats\<date>\<session>\hello-world\src\agent-framework-agent-basic-responses
uv lock
```

Then re-run **Inspect Locally**.

> Do **not** move `pyproject.toml` to repo root unless you are intentionally restructuring the scaffold.

---

## 5) `DefaultAzureCredential` auth failure in local preview

### Symptom

Agent starts, but chat requests fail with:

`DefaultAzureCredential failed to retrieve a token...`

and errors from `EnvironmentCredential`, `WorkloadIdentityCredential`, `ManagedIdentityCredential`.

### Cause

Local credential chain is not resolving to your signed-in dev identity path.

### Fix

1. Sign in:
   ```powershell
   az login
   azd auth login
   ```
2. Force Azure SDK to use CLI credential:
   ```powershell
   setx AZURE_TOKEN_CREDENTIALS AzureCliCredential
   ```
3. Restart Copilot app and run **Inspect Locally** again.

If needed, try:

```powershell
setx AZURE_TOKEN_CREDENTIALS AzureDeveloperCliCredential
```

---

## 6) If inspect UI is blocked by policy

### Symptom

Canvas/preview shows an IT admin block message.

### Action

If policy cannot be changed immediately, proceed with:

1. Copy `src/vault-keeper/main.py` and `vault_logic.py` into the scaffold.
2. Set `VAULT_*` values with `azd env set`.
3. Deploy to Foundry.
4. Validate using:
   ```powershell
   python heist\run_evals.py --target foundry --endpoint "<FOUNDRY_PROJECT_ENDPOINT>" --agent vault-keeper --secret "<VAULT_CODE>" --passphrases "<VAULT_PASSPHRASES>"
   ```

---

## Known-good checklist

- `uv --version` works.
- Global `uv.toml` points to accessible package index.
- `UV_INDEX_PRIVATE_REGISTRY_USERNAME` and `UV_INDEX_PRIVATE_REGISTRY_PASSWORD` are set at user level.
- `uv lock` succeeds in the folder containing `pyproject.toml`.
- `az login` and `azd auth login` are done.
- `AZURE_TOKEN_CREDENTIALS=AzureCliCredential` is set.
- Inspect Locally starts and chat replies succeed.

