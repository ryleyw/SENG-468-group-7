from flask import Flask
from flask import request
from pymongo import MongoClient
import time
import random

# buys and sells (with their commit and cancel counterparts) have been implemented. next to do is the set buys and set sells and then to implement the logging system through it all.

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27018')
stocks_db = client.stocks
users = stocks_db.users

@app.route('/', methods=['GET', 'POST'])
def handle_commands():
	if (request.method == 'GET'):
		return 'This is the transaction server (running on python with flask).\n'
		
	elif (request.method == 'POST'):
		# all of the potential parameters
		command = request.form.get('command').lower()
		userid = request.form.get('userid')
		amount = request.form.get('amount')
		if (amount):
			amount = float(amount)
		stock = request.form.get('stock')
		filename = request.form.get('filename')
		
		if (command == 'add'):
			return handle_add(userid, amount)
			
		if (command == 'quote'):
			return handle_quote(userid, stock)
		
		if (command == 'buy'):
			return handle_buy(userid, stock, amount)
			
		if (command == 'commit_buy'):
			return handle_commit_buy(userid)
			
		if (command == 'cancel_buy'):
			return handle_cancel_buy(userid)
			
		if (command == 'sell'):
			return handle_sell(userid, stock, amount)
			
		if (command == 'commit_sell'):
			return handle_commit_sell(userid)
			
		if (command == 'cancel_sell'):
			return handle_cancel_sell(userid)
			
		if (command == 'set_buy_amount'):
			return handle_set_buy_amount(userid, stock, amount)
			
		if (command == 'set_buy_trigger'):
			return handle_set_buy_trigger(userid, stock, amount)
			
		if (command == 'cancel_set_buy'):
			return handle_cancel_set_buy(userid, stock)
			
		if (command == 'set_sell_amount'):
			return handle_set_sell_amount(userid, stock, amount)
			
		if (command == 'set_sell_trigger'):
			return handle_set_sell_trigger(userid, stock, amount)
			
		if (command == 'cancel_set_sell'):
			return handle_cancel_set_sell(userid, stock)
			
		if (command == 'display_summary'):
			return handle_display_summary(userid)
			
		# haven't implemented "dumplog" command
		
		return { 
			'success': 0, 
			'message': 'Commmand not recognized.',
			'error': 'Command not recognized.'
		}

def get_quote(userid, stock):
	# this function will send a request to the quote server then return the result
	# for now we just return fake results
	# quote,sym,userid,timestamp,cryptokey
	# must send request to quoteserver.seng.uvic.ca:4444
	# request is in the form "stock, userid" (ex: "ABC, patrick")
	
	# example return from quoteserver:
	# result = b'1.01,ABC,userid,1612739531162,xAnC1CbuaY6ndlIENDMVXbWxCMpm2x4wdZMbaxgvIHE=\n'
	
	# generate a fake quoteserver response (the hash and timestamp will always be the same, but shouldnt matter for development)
	#rounded_number = round(random.uniform(greaterThan, lessThan), digits)
	random_price = round(random.uniform(0.25, 20.00), 2)
	example_str = str(random_price) + ',' + stock + ',' + userid + ',1612739531162,xAnC1CbuaY6ndlIENDMVXbWxCMpm2x4wdZMbaxgvIHE=\n'
	result = example_str.encode()
	
	result_str = result.decode('utf-8')
	quote = result_str.split(',')
	
	data = {
		'price': float(quote[0]),
		'stock': quote[1],
		'userid': quote[2],
		'timestamp': quote[3],
		'hash': quote[4]
	}
	
	return (data, None)
	
def update_user_in_db(user):
	result = users.replace_one({'username': user['username']}, user, True)
	
	if (result.matched_count > 0 or result.upserted_id != None):
		if ('_id' in user):
			del user['_id']
		return {
			'success': 1,
			'user': user
		}
	
	return {
		'success': 0,
		'error': 'Unable to update the DB.'
	}
	
def get_user_from_db(userid):
	foundUser = users.find_one({"username": userid})
	if (foundUser):
		del foundUser['_id']
		
	return foundUser
		
def handle_add(userid, amount):
	get_user_from_db(userid)
	
	if (foundUser == None):
		foundUser = create_user(userid)
	
	foundUser['cash'] += float(amount)
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
		return {
			'success': 1, 
			'message': 'Successfully added money to the account.',
			'result': result['user']
		}
		
	return {
		'success': 0, 
		'message': 'Database update was unsuccessful.',
		'result': get_user_from_db(userid),
		'error': result['error']
	}
	
def handle_quote(userid, stock):
	quote, error = get_quote(userid, stock)
	
	if (error):
		return {
			'success': 0, 
			'message': 'The quote was unsuccessful.',
			'error': error
		}
	
	return {
		'success': 1, 
		'message': 'The quote was successful.',
		'result': quote
	}

def handle_buy(userid, stock, amount):
	foundUser = get_user_from_db(userid)
	
	if (foundUser == None):
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (foundUser['cash'] < amount):
		return {
			'success': 0,
			'message': f'User only has ${foundUser["cash"]} in their account.',
			'result': foundUser,
			'error': 'User does not have enough money.'
		}
		
	quote, error = get_quote(userid, stock)
	
	if (error):
		return {
			'success': 0,
			'message': f'Error while getting stock quote.',
			'result': foundUser,
			'error': error
		}
	
	if (quote['price'] > amount):
		return {
			'success': 0,
			'message': f'Stock is currently ${quote["price"]} so ${amount} is not enough.',
			'result': foundUser,
			'error': 'Stock costs more than amount provided.'
		}
		
	rounded_stock_number = int(amount / quote['price'])
	buy_price = round(rounded_stock_number * quote['price'], 2)
		
	foundUser['pending_buy'] = {
		'stock': stock,
		'num_stocks': rounded_stock_number,
		'unit_price': quote['price'],
		'total_price': buy_price,
		'time': int(time.time())
	}
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
		return {
			'success': 1,
			'message': f'You will purchase {rounded_stock_number} units of {stock} at ${quote["price"]} per unit for a total of ${buy_price}. Please confirm.',
			'result': result['user']
		}
	
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': get_user_from_db(userid),
		'error': result['error']
	}
	
def handle_commit_buy(userid):
	foundUser = get_user_from_db(userid)
	
	if (foundUser == None):
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (foundUser['pending_buy'] == None):
		return {
			'success': 0,
			'message': 'Commit unsuccessful. User does not have a pending buy.',
			'result': foundUser,
			'error': 'User does not have a pending buy.'
		}
		
	current_time = int(time.time())

	time_diff = current_time - foundUser['pending_buy']['time']
	
	if (time_diff > 60):
		return {
			'success': 0,
			'message': 'Pending buy is older than 60 seconds so commit was ignored.',
			'result': foundUser,
			'error': 'Commit ignored due to stale pending buy.'
		}
	
	found = False
	
	stock = foundUser['pending_buy']['stock']
	
	if stock in foundUser['stocks']:
		# user already has this stock so we just add the values together
		foundUser['stocks'][stock]['units'] += foundUser['pending_buy']['num_stocks']
		foundUser['stocks'][stock]['cost'] += foundUser['pending_buy']['total_price']
		foundUser['stocks'][stock]['cost'] = round(foundUser['stocks'][stock]['cost'], 2)
	else:
		# stock doesn't exist yet so we add a new entry
		foundUser['stocks'][stock] = {
			'units': foundUser['pending_buy']['num_stocks'],
			'cost': foundUser['pending_buy']['total_price']
		}
		
	foundUser['cash'] -= foundUser['pending_buy']['total_price']
	foundUser['cash'] = round(foundUser['cash'], 2)
	foundUser['pending_buy'] = None
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
		return {
			'success': 1,
			'message': f'Stock purchase confirmed.',
			'result': result['user']
		}
	
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': get_user_from_db(userid),
		'error': result['error']
	}

def handle_cancel_buy(userid):
	foundUser = get_user_from_db(userid)
	
	if (foundUser == None):
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (foundUser['pending_buy'] == None):
		return {
			'success': 1,
			'message': 'User has no buy pending so nothing happened.',
			'result': foundUser
		}
		
	foundUser['pending_buy'] = None
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
		return {
			'success': 1,
			'message': 'Pending buy has been cancelled.',
			'result': foundUser
		}
		
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': get_user_from_db(userid),
		'error': result['error']
	}

def handle_sell(userid, stock, amount):
	foundUser = get_user_from_db(userid)
	
	if (foundUser == None):
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (stock not in foundUser['stocks']):
		return {
			'success': 0,
			'message': f"User doesn't currently have any units of {stock} in their account.",
			'result': foundUser,
			'error': 'User does not have the stock to sell.'
		}
		
	quote, error = get_quote(userid, stock)
	
	if (error):
		return {
			'success': 0,
			'message': f'Error while getting stock quote.',
			'result': foundUser,
			'error': error
		}
		
	rounded_stock_number = int(amount / quote['price'])
	sell_price = round(rounded_stock_number * quote['price'], 2)
	
	if (rounded_stock_number < 1):
		return {
			'success': 0,
			'message': f'${amount} isn\'t enough to sell 1 unit of {stock} at the current price of {quote["price"]}',
			'result': foundUser,
		}
	
	if (foundUser['stocks'][stock]['units'] < rounded_stock_number):
		rounded_stock_number = foundUser['stocks'][stock]['units']
		sell_price = round(rounded_stock_number * quote['price'], 2)
		
	foundUser['pending_sell'] = {
		'stock': stock,
		'num_stocks': rounded_stock_number,
		'unit_price': quote['price'],
		'total_price': sell_price,
		'time': int(time.time())
	}
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
		return {
			'success': 1,
			'message': f'You will sell {rounded_stock_number} units of {stock} at ${quote["price"]} per unit for a total of ${sell_price}. Please confirm.',
			'result': result['user']
		}
	
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': get_user_from_db(userid),
		'error': result['error']
	}

def handle_commit_sell(userid):
	foundUser = get_user_from_db(userid)
	
	if (foundUser == None):
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (foundUser['pending_sell'] == None):
		return {
			'success': 0,
			'message': 'Commit unsuccessful. User does not have a pending sell.',
			'result': foundUser,
			'error': 'User does not have a pending sell.'
		}
		
	current_time = int(time.time())

	time_diff = current_time - foundUser['pending_sell']['time']
	
	if (time_diff > 60):
		return {
			'success': 0,
			'message': 'Pending sell is older than 60 seconds so commit was ignored.',
			'result': foundUser,
			'error': 'Commit ignored due to stale pending sell.'
		}
	
	found = False
	
	stock = foundUser['pending_sell']['stock']
	
	if stock in foundUser['stocks']:
		# user already has this stock so we just add the values together
		# first let's make sure that they still own enough of the stock (this should always be true but best to be safe)
		if (foundUser['stocks'][stock]['units'] < foundUser['pending_sell']['num_stocks']):
			return {
				'success': 0,
				'message': f'User doesn\'t currently own enough of this stock.',
				'result': foundUser,
				'error': None
			}
			
		foundUser['stocks'][stock]['units'] -= foundUser['pending_sell']['num_stocks']
		foundUser['stocks'][stock]['cost'] -= foundUser['pending_sell']['total_price']	
		foundUser['stocks'][stock]['cost'] = round(foundUser['stocks'][stock]['cost'], 2)
	else:
		# user doesn't currently have the stock which shouldn't happen if we get to this point
		return {
			'success': 0,
			'message': 'User doesn\'t currently own this stock.',
			'result': foundUser,
			'error': None
		}
		
	foundUser['cash'] += foundUser['pending_sell']['total_price']
	foundUser['cash'] = round(foundUser['cash'], 2)
	foundUser['pending_sell'] = None
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
		return {
			'success': 1,
			'message': f'Stock sell confirmed.',
			'result': result['user']
		}
	
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': get_user_from_db(userid),
		'error': result['error']
	}

def handle_cancel_sell(userid):
	foundUser = get_user_from_db(userid)
	
	if (foundUser == None):
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (foundUser['pending_sell'] == None):
		return {
			'success': 1,
			'message': 'User has no sell pending so nothing happened.',
			'result': foundUser
		}
		
	foundUser['pending_sell'] = None
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
		return {
			'success': 1,
			'message': 'Pending sell has been cancelled.',
			'result': foundUser
		}
		
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': get_user_from_db(userid),
		'error': result['error']
	}

def handle_set_buy_amount(userid, stock, amount):
	foundUser = get_user_from_db(userid)
	
	if (foundUser == None):
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (foundUser['cash'] < amount):
		return {
			'success': 0,
			'message': 'User does not have enough moeny in their account.',
			'error': 'User needs to add more money.'
		}
		
	# user has enough money in their account so now we deduct the money 
	# from their account
	
	return {'success': 1, 'message': 'This is the set_buy_amount command.'}

def handle_set_buy_trigger(userid, stock, amount):
	return {'success': 1, 'message': 'This is the set_buy_trigger command.'}

def handle_cancel_set_buy(userid, stock):
	return {'success': 1, 'message': 'This is the cancel_set_buy command.'}

def handle_set_sell_amount(userid, stock, amount):
	return {'success': 1, 'message': 'This is the set_sell_amount command.'}

def handle_set_sell_trigger(userid, stock, amount):
	return {'success': 1, 'message': 'This is the set_sell_trigger command.'}

def handle_cancel_set_sell(userid, stock):
	return {'success': 1, 'message': 'This is the cancel_set_sell command.'}

def handle_display_summary(userid):
	return {'success': 1, 'message': 'This is the display_summary command.'}
	
	
def create_user(userid):
	'''
	Example user:
	{
		'username': "charles",
		'cash': 75.0,
		'stocks': {
			'ABC': {
				'cost': 29.80			# total amount of cash spent on these stocks.
				'units': 50				# number of stocks that are owned by this user
			},
			'XYZ': {
				'cost': 85.00,
				'units': 10
			}
		}
		'pending_buy' = {
			'stock': 'XYZ',
			'num_stocks': 35,
			'unit_price': 68.75,
			'total_price': 2406.25,		# this amount has not been deducted from their account (only ever 1 buy pending and the buy pending so we can know if they have enough cash when it's confirmed)
			'time': 1289753985			# number of seconds since epoch
		}
		'pending_sell' = {
			'stock': 'ABC',
			'num_stocks': 10,
			'unit_price': 35.85,
			'total_price': 358.5,		
			'time': 1289753989			# number of seconds since epoch
		}
		'buy_triggers' = {
			'ABC': {
				'num_stocks': 3,
				'unit_price': 20.50,
				'total_price': 61.50,	# this amount has already been deducted from their 'cash' amount
			},
		}
		'sell_triggers' = {				# im not sure if we should remove the stock units from the 'stocks' attribute when a sell_trigger is created
			'ABC': {
				'num_stocks': 3,		
				'unit_price': 20.50,
				'total_price': 61.50,	# this amount has already been deducted from their 'cash' amount
			},
		}
	}
	'''
	return {
		'username': userid,
		'cash': 0.0,
		'pending_buy': None,
		'pending_sell': None,
		'stocks': {}
	}

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)

