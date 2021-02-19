import requests
import json

def print_response(text):
	obj = json.loads(text)

	if ('message' in obj):
		print(obj['message'])
		
	if ('data' in obj):
		if ('success' in obj['data']):
			print(obj['data']['success'])
		if ('message' in obj['data']):
			print(obj['data']['message'])
		if ('result' in obj['data']):
			print(obj['data']['result'])
		if ('error' in obj['data']):
			print(obj['data']['error'])

url = 'http://localhost:80/api/command/' 	# docker swarm web app
#url = 'http://localhost:81'					# docker swarm transaction server

data = {
    'command': 'get_info',
}

response = requests.post(url, json = data)

print(response.text)

'''
data = {
    'command': 'AdD',
    'userid': 'basics',
    'amount': 500.00
}

response = requests.post(url, json = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'buy',
	'userid': 'basics',
	'stock': 'ABC',
	'amount': 178.50
}

response = requests.post(url, data = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'commit_buy',
	'userid': 'basics',
}

response = requests.post(url, data = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'buy',
	'userid': 'basics',
	'stock': 'XYZ',
	'amount': 65.00
}

response = requests.post(url, data = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'cancel_buy',
	'userid': 'basics',
}

response = requests.post(url, data = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'sell',
	'userid': 'basics',
	'stock': 'ABC',
	'amount': 35.00
}

response = requests.post(url, data = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'commit_sell',
	'userid': 'basics',
}

response = requests.post(url, data = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'sell',
	'userid': 'basics',
	'stock': 'ABC',
	'amount': 15.00
}

response = requests.post(url, data = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'cancel_sell',
	'userid': 'basics',
}

response = requests.post(url, data = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'set_buy_amount',
	'userid': 'basics',
	'stock': 'ABC',
	'amount': 55.00
}

response = requests.post(url, data = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'set_buy_trigger',
	'userid': 'basics',
	'stock': 'ABC',
	'amount': 12.00
}

response = requests.post(url, data = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'cancel_set_buy',
	'userid': 'basics',
	'stock': 'ABC'
}

response = requests.post(url, data = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'set_sell_amount',
	'userid': 'basics',
	'stock': 'ABC',
	'amount': 2
}

response = requests.post(url, data = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'set_sell_trigger',
	'userid': 'basics',
	'stock': 'ABC',
	'amount': 18.00
}

response = requests.post(url, data = data)

print_response(response.text)

print('\n\n-----------------------------------\n\n')

data = {
	'command': 'cancel_set_sell',
	'userid': 'basics',
	'stock': 'ABC'
}

response = requests.post(url, data = data)

print_response(response.text)'''