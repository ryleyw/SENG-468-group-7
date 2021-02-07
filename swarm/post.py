import requests

url = 'http://localhost:5000/'
data = {
    'command': 'AdD',
    'userid': 'basics',
    'amount': 50.00
}

response = requests.post(url, data = data)

print(response.text)