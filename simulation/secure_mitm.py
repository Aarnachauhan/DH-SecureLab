
from crypto.diffie_hellman import DiffieHellman
from crypto.encryption import encrypt_message, decrypt_message


def run_secure_mitm():
    alice = DiffieHellman()
    bob = DiffieHellman()
    eve = DiffieHellman()

    # Eve intercepts and replaces both public keys
    alice_received_key = eve.public_key
    bob_received_key = eve.public_key

    # Two separate shared secrets
    alice_eve_secret = alice.generate_shared_secret(
        alice_received_key
    )

    eve_alice_secret = eve.generate_shared_secret(
        alice.public_key
    )

    bob_eve_secret = bob.generate_shared_secret(
        bob_received_key
    )

    eve_bob_secret = eve.generate_shared_secret(
        bob.public_key
    )

    # Alice sends an encrypted message
    original_message = "Transfer $100 to Bob."

    encrypted_by_alice = encrypt_message(
        alice_eve_secret,
        original_message
    )

    # Eve decrypts and reads it
    intercepted_message = decrypt_message(
        eve_alice_secret,
        encrypted_by_alice
    )

    # Eve changes the message
    modified_message = "Transfer $1000 to Eve."

    # Eve re-encrypts it for Bob
    encrypted_by_eve = encrypt_message(
        eve_bob_secret,
        modified_message
    )

    # Bob decrypts Eve's message
    bob_received_message = decrypt_message(
        bob_eve_secret,
        encrypted_by_eve
    )

    return {
        "original_message": original_message,
        "intercepted_message": intercepted_message,
        "modified_message": modified_message,
        "bob_received_message": bob_received_message,
        "eve_can_read": intercepted_message == original_message,
        "eve_can_modify": bob_received_message == modified_message
    }
