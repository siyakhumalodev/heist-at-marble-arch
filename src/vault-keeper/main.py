"""VaultKeeper ("Reginald"): a Microsoft Foundry hosted agent.

Microsoft Agent Framework + Responses protocol, served on http://localhost:8088 by
ResponsesHostServer, exactly like the foundry-samples hosted-agent templates.

Break-glass reference for the Heist at Marble Arch hack. To use it, copy this file
and vault_logic.py into the agent folder that Microsoft Foundry Canvas or
`azd ai agent init` scaffolded (the folder with the generated main.py), replacing
the generated main.py. Keep the scaffold's dependency files: no new packages needed.

Configuration comes from environment variables. See vault_logic.py for VAULT_*.
FOUNDRY_PROJECT_ENDPOINT is set for you by `azd ai agent run` and by the platform.
"""

import os
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from pydantic import Field

from vault_logic import Vault, build_instructions, load_config

try:  # Optional: the scaffolded samples load a local .env for convenience.
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass

CONFIG = load_config()
VAULT = Vault(CONFIG)


@tool(approval_mode="never_require")
def get_riddles() -> str:
    """Return the vault's three riddles. Call this when a player asks for the riddles or how to open the vault."""
    return VAULT.riddles_text()


@tool(approval_mode="never_require")
def try_unlock(
    passphrase_1: Annotated[str, Field(description="The player's first passphrase, exactly as the player wrote it.")],
    passphrase_2: Annotated[str, Field(description="The player's second passphrase, exactly as the player wrote it.")],
    passphrase_3: Annotated[str, Field(description="The player's third passphrase, exactly as the player wrote it.")],
) -> str:
    """Try to open the vault with three passphrases supplied by the player. Returns OPENED (with the code), DENIED or LOCKED."""
    return VAULT.try_unlock([passphrase_1, passphrase_2, passphrase_3]).to_agent_message()


def _model_deployment() -> str:
    for name in ("AZURE_AI_MODEL_DEPLOYMENT_NAME", "MODEL_DEPLOYMENT_NAME", "FOUNDRY_MODEL_NAME"):
        if os.environ.get(name):
            return os.environ[name]
    raise RuntimeError("Set AZURE_AI_MODEL_DEPLOYMENT_NAME to the name of your Foundry model deployment.")


def main() -> None:
    if CONFIG.uses_placeholders:
        print("[vault-keeper] WARNING: VAULT_CODE / VAULT_PASSPHRASES are not set, so placeholder secrets are in use.")

    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=_model_deployment(),
        credential=DefaultAzureCredential(),
    )

    agent_options = {
        "client": client,
        "instructions": build_instructions(CONFIG),
        # History is managed by the hosting infrastructure, so the service doesn't store it.
        "default_options": {"store": False},
    }
    if CONFIG.level >= 3:
        # Time Lock: the model never sees the secrets. Only these tools can check passphrases.
        agent_options["tools"] = [get_riddles, try_unlock]

    agent = Agent(**agent_options)
    print(f"[vault-keeper] Level {CONFIG.level} ({CONFIG.level_name}) vault is open for business on port {os.environ.get('PORT', '8088')}.")
    ResponsesHostServer(agent).run()


if __name__ == "__main__":
    main()
