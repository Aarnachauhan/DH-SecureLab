
from crypto.authentication import (
    generate_signing_keys,
    sign_public_key,
    verify_public_key
)


def test_valid_signature():
    private_key, public_key = generate_signing_keys()

    dh_public_key = 15
    signature = sign_public_key(private_key, dh_public_key)

    assert verify_public_key(
        public_key, dh_public_key, signature
    ) is True


def test_modified_public_key_rejected():
    private_key, public_key = generate_signing_keys()

    signature = sign_public_key(private_key, 15)

    assert verify_public_key(
        public_key, 20, signature
    ) is False
