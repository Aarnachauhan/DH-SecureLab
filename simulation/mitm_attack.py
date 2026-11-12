
from crypto.diffie_hellman import DiffieHellman


def run_mitm_attack():

    # Step 1: Create participants
    alice = DiffieHellman()
    bob = DiffieHellman()
    eve = DiffieHellman()

    # Step 2: Eve intercepts public keys
    # Alice receives Eve's public key instead of Bob's
    alice_received_key = eve.public_key

    # Bob receives Eve's public key instead of Alice's
    bob_received_key = eve.public_key

    # Step 3: Calculate shared secrets
    alice_secret = alice.generate_shared_secret(
        alice_received_key
    )

    bob_secret = bob.generate_shared_secret(
        bob_received_key
    )

    # Eve calculates separate secrets
    eve_alice_secret = eve.generate_shared_secret(
        alice.public_key
    )

    eve_bob_secret = eve.generate_shared_secret(
        bob.public_key
    )

    return {
        "alice_secret": alice_secret,
        "bob_secret": bob_secret,
        "eve_alice_secret": eve_alice_secret,
        "eve_bob_secret": eve_bob_secret,
        "eve_can_read_alice": alice_secret == eve_alice_secret,
        "eve_can_read_bob": bob_secret == eve_bob_secret
    }
