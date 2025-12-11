import requests

# Read encrypted seed from file
with open("encrypted_seed.txt", "r") as f:
    encrypted_seed = f.read().strip()

url = "http://localhost:8080/decrypt-seed"

payload = {"encrypted_seed": encrypted_seed}

response = requests.post(url, json=payload)

print("Status:", response.status_code)
print("Response:", response.text)
