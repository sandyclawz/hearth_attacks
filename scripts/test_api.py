import requests


url = "http://127.0.0.1:8000/predict"

payload = {
    "file_path": "data/raw/heart_test.csv"
}

response = requests.post(url, json=payload)

print("Status code:", response.status_code)
print(response.json())