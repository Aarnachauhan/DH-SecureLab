
from crypto.diffie_hellman import DiffieHellman


def test_dh_shared_secrets_match():
    alice = DiffieHellman()
    bob = DiffieHellman()

    alice_secret = alice.generate_shared_secret(bob.public_key)
    bob_secret = bob.generate_shared_secret(alice.public_key)

    assert alice_secret == bob_secret


def test_dh_invalid_public_key():
    alice = DiffieHellman()

    try:
        alice.generate_shared_secret(1)
        assert False, "Expected ValueError"
    except ValueError:
        assert True
