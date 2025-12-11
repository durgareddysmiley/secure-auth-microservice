import requests

# 1. Get a valid code
resp = requests.get("http://localhost:8080/generate-2fa")
code = resp.json()["code"]

print("Generated Code:", code)

# 2. Send code to verify endpoint
verify_resp = requests.post(
    "http://localhost:8080/verify-2fa",
    json={"code": code}
)

print("Verify Status:", verify_resp.status_code)
print("Verify Response:", verify_resp.text)
