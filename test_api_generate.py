import requests

response = requests.get("http://localhost:8080/generate-2fa")

print("Status:", response.status_code)
print("Response:", response.text)
