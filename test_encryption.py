
from crypto.encryption import encrypt_message, decrypt_message

shared_secret = 12345
message = "Hello Bob! This is a secure message."

print("Original Message:", message)

encrypted = encrypt_message(shared_secret, message)

print("Encrypted Message:", encrypted["ciphertext"].hex())

decrypted = decrypt_message(shared_secret, encrypted)

print("Decrypted Message:", decrypted)

print("Encryption Successful:", message == decrypted)
