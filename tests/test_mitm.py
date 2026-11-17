
from simulation.mitm_attack import run_mitm_attack


def test_mitm_attack_success():
    result = run_mitm_attack()

    assert result["eve_can_read_alice"] is True
    assert result["eve_can_read_bob"] is True


def test_mitm_creates_separate_secrets():
    result = run_mitm_attack()

    assert result["alice_secret"] == result["eve_alice_secret"]
    assert result["bob_secret"] == result["eve_bob_secret"]
