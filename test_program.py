import requests

payload = {
    "data": {
        "projects": 5,
        "workspaces": 2,
    }
}

response = requests.post(
    "http://localhost:5000/summary",
    json=payload,
    timeout=5,
)

print("Status:", response.status_code)
print("Response:", response.json())