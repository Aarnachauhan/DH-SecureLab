
from crypto.authentication import (
    generate_signing_keys,
    sign_public_key,
    verify_public_key
)

# Alice generates RSA keys
alice_private, alice_public = generate_signing_keys()

# Alice signs her DH public key
alice_dh_public_key = 15

signature = sign_public_key(
    alice_private,
    alice_dh_public_key
)

# Bob verifies Alice's signature
valid = verify_public_key(
    alice_public,
    alice_dh_public_key,
    signature
)

print("===== AUTHENTICATION TEST =====")
print("Original public key:", alice_dh_public_key)
print("Signature valid:", valid)

# Eve modifies Alice's public key
modified_key = 20

tampered = verify_public_key(
    alice_public,
    modified_key,
    signature
)

print("\n===== TAMPERING TEST =====")
print("Modified public key:", modified_key)
print("Signature valid:", tampered)
