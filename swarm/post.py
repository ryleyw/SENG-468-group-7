import requests

url = 'http://localhost:80/api/command/'
data = {
    'command': 'AdD',
    'userid': 'basics',
    'amount': 50.00
}

response = requests.post(url, data = data)

print(response.text)