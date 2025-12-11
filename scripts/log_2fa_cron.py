#!/usr/bin/env python3

import sys
import os
from datetime import datetime, timezone

# Allow cron to import modules from /app
sys.path.append("/app")

from totp_utils import generate_totp_code  # your function
from totp_utils import hex_to_base32       # if used internally


def main():
    seed_path = "/data/seed.txt"

    # 1. Read the hex seed from file
    try:
        with open(seed_path, "r") as f:
            hex_seed = f.read().strip()
    except FileNotFoundError:
        print("ERROR: seed file not found.")
        return
    except Exception as e:
        print(f"ERROR reading seed: {e}")
        return

    # 2. Generate current TOTP code
    try:
        code = generate_totp_code(hex_seed)
    except Exception as e:
        print(f"ERROR generating TOTP: {e}")
        return

    # 3. Current UTC timestamp
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # 4. Print log line (cron appends this to /cron/last_code.txt)
    print(f"{timestamp} - 2FA Code: {code}")


if __name__ == "__main__":
    main()
