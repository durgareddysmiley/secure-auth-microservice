import os
import time
from totp_utils import generate_totp_code

SEED_FILE = "/data/seed.txt"
CRON_FILE = "/cron/last_code.txt"

try:
    if not os.path.exists(SEED_FILE):
        print("Seed not found; cron skipped")
        exit(0)

    with open(SEED_FILE, "r") as f:
        seed = f.read().strip()

    code = generate_totp_code(seed)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    with open(CRON_FILE, "a") as f:
        f.write(f"{timestamp} - 2FA Code: {code}\n")

except Exception as e:
    print("Cron error:", e)
