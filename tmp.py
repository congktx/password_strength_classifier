from passlib import pwd

password = "MyP@ssw0rd123"
stats = pwd.entropy(password)

print(f"Entropy: {stats.entropy:.2f}")
print(f"Password Strength: {stats.strength:.2f}")
