
from simulation.secure_mitm import run_secure_mitm

result = run_secure_mitm()

print("===== ENCRYPTED MITM ATTACK =====")
print("Alice's Original Message:", result["original_message"])
print("Eve Intercepted:", result["intercepted_message"])
print("Eve Modified:", result["modified_message"])
print("Bob Received:", result["bob_received_message"])

print("\n===== ATTACK RESULTS =====")
print("Eve Can Read:", result["eve_can_read"])
print("Eve Can Modify:", result["eve_can_modify"])
