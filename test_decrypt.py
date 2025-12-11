from decrypt_seed import decrypt_seed, load_private_key

# Load encrypted seed from file
with open("encrypted_seed.txt", "r") as f:
    encrypted_b64 = f.read().strip()

# Load private key
private_key = load_private_key()

# Decrypt
try:
    seed = decrypt_seed(encrypted_b64, private_key)
    print("Decrypted Seed:", seed)
except Exception as e:
    print("Error:", e)
