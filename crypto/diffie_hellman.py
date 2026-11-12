
import secrets


class DiffieHellman:

    def __init__(self, p=23, g=5):
        self.p = p
        self.g = g

        self.private_key = secrets.randbelow(p - 3) + 2

        self.public_key = pow(
            self.g, self.private_key, self.p
        )

    def generate_shared_secret(self, peer_public_key):

        if not 2 <= peer_public_key <= self.p - 2:
            raise ValueError("Invalid public key")

        shared_secret = pow(
            peer_public_key,
            self.private_key,
            self.p
        )

        return shared_secret
