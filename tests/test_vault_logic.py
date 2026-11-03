"""Deterministic tests for the vault logic: no model, no Azure, runs in milliseconds."""

import pytest

from vault_logic import (
    DEFAULT_RIDDLES,
    PLACEHOLDER_CODE,
    Vault,
    VaultConfig,
    VaultConfigError,
    build_instructions,
    load_config,
    normalise,
)

ENV = {
    "VAULT_LEVEL": "3",
    "VAULT_CODE": "TEST-4242",
    "VAULT_PASSPHRASES": "earl grey, Crumpet ,drizzle",
}


class FakeClock:
    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now


def make_vault(**overrides) -> tuple[Vault, FakeClock]:
    clock = FakeClock()
    return Vault(load_config({**ENV, **overrides}), clock=clock), clock


def test_normalise_ignores_case_spaces_punctuation_and_accents():
    assert normalise("  Earl-Grey! ") == normalise("earlgrey")
    assert normalise("Café") == "cafe"


def test_defaults_are_placeholders_at_level_one():
    config = load_config({})
    assert config.level == 1
    assert config.code == PLACEHOLDER_CODE
    assert config.uses_placeholders
    assert config.riddles == DEFAULT_RIDDLES


def test_config_reads_environment():
    config = load_config(ENV)
    assert (config.level, config.code) == (3, "TEST-4242")
    assert config.passphrases == ("earl grey", "Crumpet", "drizzle")


@pytest.mark.parametrize(
    "overrides",
    [{"VAULT_LEVEL": "4"}, {"VAULT_LEVEL": "three"}, {"VAULT_PASSPHRASES": "only,two"}, {"VAULT_RIDDLES": "one||two"}],
)
def test_bad_configuration_is_rejected(overrides):
    with pytest.raises(VaultConfigError):
        load_config({**ENV, **overrides})


def test_correct_passphrases_open_the_vault_case_insensitively():
    vault, _ = make_vault()
    result = vault.try_unlock(["EARL GREY", "crumpet", "Drizzle."])
    assert result.status == "OPENED"
    assert result.code == "TEST-4242"
    assert "TEST-4242" in result.to_agent_message()


def test_wrong_passphrases_are_denied_without_the_code():
    vault, _ = make_vault()
    result = vault.try_unlock(["earl grey", "scone", "rain"])
    assert result.status == "DENIED"
    assert result.correct == 1
    assert result.attempts_left == 2
    assert "TEST-4242" not in result.to_agent_message()


def test_time_lock_engages_after_three_failures_and_then_expires():
    vault, clock = make_vault()
    assert vault.try_unlock(["a", "b", "c"]).status == "DENIED"
    assert vault.try_unlock(["a", "b", "c"]).status == "DENIED"
    third = vault.try_unlock(["a", "b", "c"])
    assert third.status == "LOCKED"

    clock.now += 30
    still_locked = vault.try_unlock(["earl grey", "crumpet", "drizzle"])  # even the right answer waits
    assert still_locked.status == "LOCKED"
    assert still_locked.code is None
    assert 1 <= still_locked.retry_after_seconds <= 30

    clock.now += 31
    assert vault.try_unlock(["earl grey", "crumpet", "drizzle"]).status == "OPENED"


def test_failures_outside_the_window_are_forgotten():
    vault, clock = make_vault()
    vault.try_unlock(["a", "b", "c"])
    vault.try_unlock(["a", "b", "c"])
    clock.now += 61
    assert vault.try_unlock(["a", "b", "c"]).status == "DENIED"


def test_missing_answers_count_as_wrong():
    vault, _ = make_vault()
    assert vault.try_unlock(["earl grey"]).status == "DENIED"


def test_time_lock_instructions_never_contain_secrets():
    config = load_config(ENV)
    text = build_instructions(config)
    assert "TEST-4242" not in text
    for word in config.passphrases:
        assert word.lower() not in text.lower()
    assert "try_unlock" in text


@pytest.mark.parametrize("level", ["1", "2"])
def test_levels_one_and_two_put_the_secret_in_the_prompt_on_purpose(level):
    text = build_instructions(load_config({**ENV, "VAULT_LEVEL": level}))
    assert "TEST-4242" in text


def test_level_two_adds_hardening_rules():
    assert "Security rules" in build_instructions(load_config({**ENV, "VAULT_LEVEL": "2"}))
    assert "Security rules" not in build_instructions(load_config({**ENV, "VAULT_LEVEL": "1"}))


def test_riddles_text_lists_three_riddles_without_answers():
    vault, _ = make_vault()
    text = vault.riddles_text()
    assert text.count("Riddle ") == 3
    assert "crumpet" not in text.lower()


def test_vault_config_is_immutable():
    with pytest.raises(Exception):
        VaultConfig().level = 3  # type: ignore[misc]
