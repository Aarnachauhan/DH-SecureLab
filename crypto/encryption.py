
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def derive_aes_key(shared_secret):
    """
    Convert the DH shared secret into a 256-bit AES key.
    """
    secret_bytes = shared_secret.to_bytes(
        (shared_secret.bit_length() + 7) // 8,
        byteorder="big"
    )

    # Ensure even small educational secrets have at least one byte.
    if not secret_bytes:
        secret_bytes = b"\x00"

    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"DH-SecureLab-AES-GCM"
    ).derive(secret_bytes)


def encrypt_message(shared_secret, message):
    """
    Encrypt a message using AES-256-GCM.
    """
    key = derive_aes_key(shared_secret)
    aesgcm = AESGCM(key)

    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(
        nonce,
        message.encode("utf-8"),
        None
    )

    return {
        "nonce": nonce,
        "ciphertext": ciphertext
    }


def decrypt_message(shared_secret, encrypted_data):
    """
    Decrypt an AES-GCM encrypted message.
    """
    key = derive_aes_key(shared_secret)
    aesgcm = AESGCM(key)

    plaintext = aesgcm.decrypt(
        encrypted_data["nonce"],
        encrypted_data["ciphertext"],
        None
    )

    return plaintext.decode("utf-8")
