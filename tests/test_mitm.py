
from simulation.mitm_attack import run_mitm_attack


result = run_mitm_attack()

print("===== MITM ATTACK SIMULATION =====")

print("Alice's Secret:", result["alice_secret"])
print("Bob's Secret:", result["bob_secret"])

print("\nEve-Alice Secret:", result["eve_alice_secret"])
print("Eve-Bob Secret:", result["eve_bob_secret"])

print("\n===== ATTACK RESULTS =====")

print("Eve can communicate with Alice:",
      result["eve_can_read_alice"])

print("Eve can communicate with Bob:",
      result["eve_can_read_bob"])
