import base64
import pyotp

def hex_to_base32(hex_seed: str) -> str:
    """Convert 64-character hex seed to Base32 encoding."""
    # Convert hex string → bytes
    seed_bytes = bytes.fromhex(hex_seed)

    # Convert bytes → base32 string
    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")

    return base32_seed


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current TOTP code from hex seed.
    TOTP settings: SHA-1, 30s period, 6 digits (default pyotp values).
    """

    # 1. Convert hex → base32
    base32_seed = hex_to_base32(hex_seed)

    # 2. Create TOTP generator (pyotp uses SHA-1, 30s, 6 digits by default)
    totp = pyotp.TOTP(base32_seed)

    # 3. Return current TOTP code
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify code with ±1 period (default).
    valid_window = 1 → accepts:
        previous 30s window,
        current 30s window,
        next 30s window
    """

    # 1. Convert hex → base32
    base32_seed = hex_to_base32(hex_seed)

    # 2. Create TOTP generator
    totp = pyotp.TOTP(base32_seed)

    # 3. Verify with time window tolerance
    return totp.verify(code, valid_window=valid_window)
