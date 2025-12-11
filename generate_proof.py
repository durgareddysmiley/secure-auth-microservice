import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


# ----------------------------------------------------
# Load commit hash
# ----------------------------------------------------
with open("commit_hash.txt", "r") as f:
    commit_hash = f.read().strip()  # 40-char hex string


# ----------------------------------------------------
# Load student private key (RSA-PSS signing)
# ----------------------------------------------------
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )


# ----------------------------------------------------
# SIGN commit hash using RSA-PSS + SHA-256
# ----------------------------------------------------
signature = private_key.sign(
    commit_hash.encode("utf-8"),  # sign ASCII string
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)


# ----------------------------------------------------
# Load instructor public key (RSA-OAEP encryption)
# ----------------------------------------------------
with open("instructor_public.pem", "rb") as f:
    instructor_pub = serialization.load_pem_public_key(f.read())


# ----------------------------------------------------
# Encrypt signature using RSA-OAEP + SHA-256
# ----------------------------------------------------
encrypted = instructor_pub.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)


# ----------------------------------------------------
# Base64 encode final encrypted signature
# ----------------------------------------------------
b64_output = base64.b64encode(encrypted).decode("utf-8")

print("\n=== COMMIT PROOF OUTPUT ===")
print("Commit Hash:", commit_hash)
print("Encrypted Signature:", b64_output)
print("\nCopy this EXACT Base64 string for submission.\n")
