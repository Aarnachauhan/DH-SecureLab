
from crypto.diffie_hellman import DiffieHellman

# Create Alice and Bob
alice = DiffieHellman()
bob = DiffieHellman()

# Generate shared secrets
alice_secret = alice.generate_shared_secret(bob.public_key)
bob_secret = bob.generate_shared_secret(alice.public_key)

print("----- ALICE -----")
print("Private Key:", alice.private_key)
print("Public Key:", alice.public_key)

print("\n----- BOB -----")
print("Private Key:", bob.private_key)
print("Public Key:", bob.public_key)

print("\n----- SHARED SECRET -----")
print("Alice's Secret:", alice_secret)
print("Bob's Secret:", bob_secret)

print("\nKeys Match:", alice_secret == bob_secret)
