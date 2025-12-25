import requests
import json
import os

key = "AIzaSyDjlh2ey_ghpSNIsRdzC_pS3Jhl5Ge7cic"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
headers = {"Content-Type": "application/json"}
data = {
    "contents": [{
        "parts": [{"text": "Explain how AI works in a few words"}]
    }]
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response:", response.json()['candidates'][0]['content']['parts'][0]['text'])
    else:
        print("Error:", response.text)
except Exception as e:
    print("Exception:", str(e))
