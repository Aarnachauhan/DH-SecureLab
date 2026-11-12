
from crypto.diffie_hellman import DiffieHellman

from crypto.authentication import (
    generate_signing_keys,
    sign_public_key,
    verify_public_key
)


def run_authenticated_exchange(attack=False):

    # Step 1: Generate DH keys
    alice = DiffieHellman()
    bob = DiffieHellman()
    eve = DiffieHellman()

    # Step 2: Generate trusted RSA signing keys
    alice_private, alice_public = generate_signing_keys()
    bob_private, bob_public = generate_signing_keys()

    # Step 3: Sign original DH public keys
    alice_signature = sign_public_key(
        alice_private, alice.public_key
    )

    bob_signature = sign_public_key(
        bob_private, bob.public_key
    )

    # Step 4: Simulate public key exchange
    if attack:
        alice_received_key = eve.public_key
        bob_received_key = eve.public_key
    else:
        alice_received_key = bob.public_key
        bob_received_key = alice.public_key

    # Step 5: Verify signatures
    alice_verified = verify_public_key(
        bob_public,
        alice_received_key,
        bob_signature
    )

    bob_verified = verify_public_key(
        alice_public,
        bob_received_key,
        alice_signature
    )

    # Step 6: Calculate secrets only after verification
    if not alice_verified or not bob_verified:
        return {
            "authenticated": False,
            "alice_verified": alice_verified,
            "bob_verified": bob_verified,
            "message": "Exchange rejected: Authentication failed!"
        }

    alice_secret = alice.generate_shared_secret(
        alice_received_key
    )

    bob_secret = bob.generate_shared_secret(
        bob_received_key
    )

    return {
        "authenticated": True,
        "alice_verified": alice_verified,
        "bob_verified": bob_verified,
        "alice_secret": alice_secret,
        "bob_secret": bob_secret,
        "keys_match": alice_secret == bob_secret,
        "message": "Authenticated exchange successful!"
    }
