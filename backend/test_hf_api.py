from dotenv import load_dotenv
load_dotenv()

import os
import requests

hf_api_key = os.getenv("HF_API_KEY")
print("HF_API_KEY:", hf_api_key)  # Debug print

url = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {hf_api_key}"}
payload = {"inputs": "def hello_world():"}

try:
    response = requests.post(url, headers=headers, json=payload)
    print("Status code:", response.status_code)
    print("Response text:", response.text)
except Exception as e:
    print("Exception occurred:", e) 