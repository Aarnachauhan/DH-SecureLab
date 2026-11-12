
from simulation.normal_exchange import run_normal_exchange
from crypto.encryption import encrypt_message, decrypt_message

print("===== SECURE MESSAGE EXCHANGE =====")

result = run_normal_exchange()

if result["keys_match"]:
    message = "Hello Bob! This is Alice."

    encrypted = encrypt_message(
        result["alice_secret"],
        message
    )

    print("Alice's Message:", message)
    print("Encrypted Ciphertext:", encrypted["ciphertext"].hex())

    decrypted = decrypt_message(
        result["bob_secret"],
        encrypted
    )

    print("Bob Decrypted:", decrypted)
    print("Message Delivered:", message == decrypted)
else:
    print("Key exchange failed!")
