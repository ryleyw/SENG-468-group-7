import requests

url = 'http://localhost:5000/'
data = {
    'command': 'AdD',
    'userid': 'basics',
    'amount': 500.00
}

response = requests.post(url, data = data)

print(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'buy',
	'userid': 'basics',
	'stock': 'ABC',
	'amount': 178.50
}

response = requests.post(url, data = data)

print(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'commit_buy',
	'userid': 'basics',
}

response = requests.post(url, data = data)

print(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'buy',
	'userid': 'basics',
	'stock': 'XYZ',
	'amount': 65.00
}

response = requests.post(url, data = data)

print(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'commit_buy',
	'userid': 'basics',
}

response = requests.post(url, data = data)

print(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'sell',
	'userid': 'basics',
	'stock': 'ABC',
	'amount': 35.00
}

response = requests.post(url, data = data)

print(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'commit_sell',
	'userid': 'basics',
}

response = requests.post(url, data = data)

print(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'sell',
	'userid': 'basics',
	'stock': 'ABC',
	'amount': 15.00
}

response = requests.post(url, data = data)

print(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'commit_sell',
	'userid': 'basics',
}

response = requests.post(url, data = data)

print(response.text)