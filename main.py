from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import time

from decrypt_seed import decrypt_seed, load_private_key
from totp_utils import generate_totp_code, verify_totp_code

app = FastAPI()

DATA_DIR = "/data"
SEED_FILE = f"{DATA_DIR}/seed.txt"

# Ensure /data exists when running locally (Docker will mount volume)
os.makedirs(DATA_DIR, exist_ok=True)


# -------------------------------
# Request Models
# -------------------------------
class SeedRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


# -------------------------------
# Endpoint 1: POST /decrypt-seed
# -------------------------------
@app.post("/decrypt-seed")
def decrypt_seed_endpoint(req: SeedRequest):
    try:
        # Load private key
        private_key = load_private_key()

        # Decrypt seed
        hex_seed = decrypt_seed(req.encrypted_seed, private_key)

        # Save to /data/seed.txt
        with open(SEED_FILE, "w") as f:
            f.write(hex_seed)

        return {"status": "ok"}

    except Exception as e:
        print("Decryption failed:", e)
        raise HTTPException(status_code=500, detail="Decryption failed")


# -------------------------------
# Endpoint 2: GET /generate-2fa
# -------------------------------
@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    # Read stored seed
    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    # Generate TOTP
    code = generate_totp_code(hex_seed)

    # Validity seconds
    now = int(time.time())
    valid_for = 30 - (now % 30)

    return {"code": code, "valid_for": valid_for}


# -------------------------------
# Endpoint 3: POST /verify-2fa
# -------------------------------
@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    # Load seed
    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    # Verify with tolerance ±1 window
    valid = verify_totp_code(hex_seed, req.code, valid_window=1)

    return {"valid": valid}
