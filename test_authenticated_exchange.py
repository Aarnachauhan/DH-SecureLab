
from simulation.authenticated_exchange import (
    run_authenticated_exchange
)

print("===== NORMAL AUTHENTICATED EXCHANGE =====")

normal = run_authenticated_exchange(attack=False)

print("Alice Verified:", normal["alice_verified"])
print("Bob Verified:", normal["bob_verified"])
print("Alice Secret:", normal.get("alice_secret"))
print("Bob Secret:", normal.get("bob_secret"))
print("Keys Match:", normal.get("keys_match"))
print("Status:", normal["message"])


print("\n===== MITM ATTACK WITH AUTHENTICATION =====")

attack = run_authenticated_exchange(attack=True)

print("Alice Verified:", attack["alice_verified"])
print("Bob Verified:", attack["bob_verified"])
print("Status:", attack["message"])
