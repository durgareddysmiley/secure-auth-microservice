import requests

def request_seed():
    student_id = "23A91A61C6"
    github_repo_url = "https://github.com/durgareddysmiley/secure-auth-microservice"
    api_url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

    # Read your student public key
    with open("student_public.pem", "r") as f:
        public_key_pem = f.read()

    # Prepare request payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key_pem
    }

    # Send request
    response = requests.post(api_url, json=payload)

    # Check status
    if response.status_code != 200:
        print("Error:", response.text)
        return

    data = response.json()

    # Extract encrypted seed
    encrypted_seed = data.get("encrypted_seed")

    if not encrypted_seed:
        print("No encrypted seed found:", data)
        return

    # Save to file (do NOT commit this file)
    with open("encrypted_seed.txt", "w") as f:
        f.write(encrypted_seed)

    print("Encrypted seed saved to encrypted_seed.txt")

# Run it
request_seed()
