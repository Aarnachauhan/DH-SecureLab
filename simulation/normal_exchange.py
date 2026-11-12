
from crypto.diffie_hellman import DiffieHellman


def run_normal_exchange():

    # Step 1: Create Alice and Bob
    alice = DiffieHellman()
    bob = DiffieHellman()

    # Step 2: Exchange public keys
    alice_received_key = bob.public_key
    bob_received_key = alice.public_key

    # Step 3: Generate shared secrets
    alice_secret = alice.generate_shared_secret(
        alice_received_key
    )

    bob_secret = bob.generate_shared_secret(
        bob_received_key
    )

    # Step 4: Verify shared secrets
    keys_match = alice_secret == bob_secret

    # Step 5: Return simulation results
    return {
        "alice_public_key": alice.public_key,
        "bob_public_key": bob.public_key,
        "alice_secret": alice_secret,
        "bob_secret": bob_secret,
        "keys_match": keys_match
    }
