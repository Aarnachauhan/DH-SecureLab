
from simulation.normal_exchange import run_normal_exchange


result = run_normal_exchange()

print("===== NORMAL KEY EXCHANGE =====")

print("Alice Public Key:", result["alice_public_key"])
print("Bob Public Key:", result["bob_public_key"])

print("Alice Shared Secret:", result["alice_secret"])
print("Bob Shared Secret:", result["bob_secret"])

print("Keys Match:", result["keys_match"])
