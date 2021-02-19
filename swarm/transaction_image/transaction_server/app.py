from flask import Flask
from flask import request
from pymongo import MongoClient
import time
import requests
import random
import sys
import socket

fake_quote_server = False
cache_time_limit = 120 	# seconds before a cached stock quote becomes stale
cached_count = 0
total_count = 0

# to print to console, use:
#print('string here', file=sys.stderr)

# i am currently using 0 and 1 instead of true and false so that there are no
# misscomunications between mongodb, python, and js
# however it's plausible that boolean values would require less space (int might be 32 or even 64 bit, whereas bool could be 8 bit)

app = Flask(__name__)

client = MongoClient('mongodb://mongos0:27017')
stocks_db = client.stocks
users = stocks_db.users
quotes = stocks_db.quotes

transactionNum = 0
logfile = '<?xml version=\"1.0\"?>\n<log>\n'

@app.route('/', methods=['GET', 'POST'])
def handle_commands():
	if (request.method == 'GET'):
		return 'This is the transaction server (running on python with flask).\n'
		
	elif (request.method == 'POST'):
		global logfile
		global transactionNum
		timestamp = round(time.time() * 1000)
		# all of the potential parameters
		data = request.json
		
		command = data['command'].lower()
		
		if ('userid' in data): userid = data['userid']
		if ('amount' in data): amount = float(data['amount'])
		if ('stock' in data): stock = data['stock']
		if ('filename' in data): filename = data['filename']
		if ('unit_price' in data): unit_price = data['unit_price']
		
		if (command == 'add'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid,
				'amount': amount
			}
			logType = 'UserCommandType_2'
			logfile += log_data(logInput,timestamp,logType)
			return handle_add(userid, amount)
			
		if (command == 'quote'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid,
				'stock': stock
			}
			logType = 'UserCommandType_3'
			logfile += log_data(logInput,timestamp,logType)
			return handle_quote(userid, stock)
		
		if (command == 'buy'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid,
				'stock': stock,
				'amount': amount
			}
			logType = 'UserCommandType_4'
			logfile += log_data(logInput,timestamp,logType)
			return handle_buy(userid, stock, amount)
			
		if (command == 'commit_buy'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid
			}
			logType = 'UserCommandType_1'
			logfile += log_data(logInput,timestamp,logType)
			return handle_commit_buy(userid)
			
		if (command == 'cancel_buy'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid
			}
			logType = 'UserCommandType_1'
			logfile += log_data(logInput,timestamp,logType)
			return handle_cancel_buy(userid)
			
		if (command == 'sell'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid,
				'stock': stock,
				'amount': amount
			}
			logType = 'UserCommandType_4'
			logfile += log_data(logInput,timestamp,logType)
			return handle_sell(userid, stock, amount)
			
		if (command == 'commit_sell'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid
			}
			logType = 'UserCommandType_1'
			logfile += log_data(logInput,timestamp,logType)
			return handle_commit_sell(userid)
			
		if (command == 'cancel_sell'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid
			}
			logType = 'UserCommandType_1'
			logfile += log_data(logInput,timestamp,logType)
			return handle_cancel_sell(userid)
			
		if (command == 'set_buy_amount'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid,
				'stock': stock,
				'amount': amount
			}
			logType = 'UserCommandType_4'
			logfile += log_data(logInput,timestamp,logType)
			return handle_set_buy_amount(userid, stock, amount)
			
		if (command == 'set_buy_trigger'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid,
				'stock': stock,
				'amount': amount
			}
			logType = 'UserCommandType_4'
			logfile += log_data(logInput,timestamp,logType)
			return handle_set_buy_trigger(userid, stock, amount)
			
		if (command == 'cancel_set_buy'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid,
				'stock': stock
			}
			logType = 'UserCommandType_3'
			logfile += log_data(logInput,timestamp,logType)
			return handle_cancel_set_buy(userid, stock)
			
		if (command == 'set_sell_amount'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid,
				'stock': stock,
				'amount': amount
			}
			logType = 'UserCommandType_4'
			logfile += log_data(logInput,timestamp,logType)
			return handle_set_sell_amount(userid, stock, amount)
			
		if (command == 'set_sell_trigger'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid,
				'stock': stock,
				'amount': amount
			}
			logType = 'UserCommandType_4'
			logfile += log_data(logInput,timestamp,logType)
			return handle_set_sell_trigger(userid, stock, amount)
			
		if (command == 'cancel_set_sell'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid,
				'stock': stock
			}
			logType = 'UserCommandType_3'
			logfile += log_data(logInput,timestamp,logType)
			return handle_cancel_set_sell(userid, stock)
			
		if (command == 'display_summary'):
			transactionNum += 1
			logInput = {
				'command': command,
				'userid': userid
			}
			logType = 'UserCommandType_1'
			logfile += log_data(logInput,timestamp,logType)
			return handle_display_summary(userid)
			
		if (command == 'dumplog'):
			transactionNum += 1
			logInput = {
				'command': command,
				'filename': filename
			}
			logType = 'UserCommandType_0'
			logfile += log_data(logInput,timestamp,logType)
			return handle_dumplog()
		
		if (command == 'execute_buy_trigger'):
			# need to add logging code @ lyon
			return handle_execute_buy_trigger(userid, stock, unit_price)
			
		if (command == 'execute_sell_trigger'):
			# need to add logging code @ lyon
			return handle_execute_sell_trigger(userid, stock, unit_price)
			
		if (command == 'get_info'):
			return {
				'cached_count': cached_count,
				'total_count': total_count
			}
		
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
	
	global logfile
	global cached_count
	global total_count
	
	found_fresh = False
	total_count += 1
	
	# first we check the DB to see if we already have a cached value for this quote
	foundQuote = quotes.find_one({'stock': stock})
	if (foundQuote):
		# check to see if it's stale
		diff = time.time() - foundQuote['docker_timestamp']
		if (diff < cache_time_limit):
			# quote is fresh so we can use it
			found_fresh = True
			
			data = {
				'price': foundQuote['price'],
				'stock': foundQuote['stock'],
				'userid': foundQuote['userid'],
				'timestamp': foundQuote['timestamp'],
				'hash': foundQuote['hash']
			}
			cached_count += 1
			
			print(f'cached quote: {stock}', file=sys.stderr)

	if (found_fresh == False):
		if (fake_quote_server):
			# generate a fake quoteserver response (the hash and timestamp will always be the same, but shouldnt matter for development)
			# rounded_number = round(random.uniform(greaterThan, lessThan), digits)
			random_price = round(random.uniform(0.25, 20.00), 2)
			example_str = str(random_price) + ',' + stock + ',' + userid + ',1612739531162,fakequoteY6ndlIENDMVXbWxCMpm2x4wdZMbaxgvIHE=\n'
			result = example_str.encode()
		else:
			skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			skt.connect(('192.168.4.2', 4444)) # only works right now if you make a new socket each time
			msg = f'{stock},{userid}\n'
			print(f'msg: {msg}', file=sys.stderr)
			skt.send(msg.encode())
			try:
				result = skt.recv(1024)
				timestamp = round(time.time() * 1000)
			except:
				print('Quote server error')
				return (None, 'Error communicating with quote server')
			skt.close()
		
		print(f'response: {result}', file=sys.stderr)
		
		result_str = result.decode('utf-8')
		quote = result_str.split(',')
		
		data = {
			'price': float(quote[0]),
			'stock': quote[1],
			'userid': quote[2],
			'timestamp': quote[3],
			'hash': quote[4]
		}
		
		newQuote = create_quote(data['stock'], data['price'], data['userid'], data['timestamp'], data['hash'])
		quotes.replace_one({'stock': data['stock']}, newQuote, True)
	
	logType = 'QuoteServerType'
	logfile += log_data(data,timestamp,logType)

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
	global logfile

	foundUser = get_user_from_db(userid)
	
	if (foundUser == None):
		foundUser = create_user(userid)
	
	foundUser['cash'] += float(amount)
	
	result = update_user_in_db(foundUser)

	timestamp = round(time.time() * 1000)
	
	if (result['success'] == 1):
		logInput = {
			'action': 'add',
			'userid': userid,
			'amount': amount
		}
		logType = 'AccountTransactionType'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 1, 
			'message': 'Successfully added money to the account.',
			'result': result['user']
		}
	
	logInput = {
		'command': 'ADD',
		'userid': userid,
		'amount': amount,
		'error':  'Could not add money to the users account.'
	}
	logType = 'ErrorEventType_2'
	logfile += log_data(logInput,timestamp,logType)
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
	global logfile

	foundUser = get_user_from_db(userid)
	
	timestamp = round(time.time() * 1000)

	if (foundUser == None):
		logInput = {
			'command': 'BUY',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User does not exist in DB.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (foundUser['cash'] < amount):
		logInput = {
			'command': 'BUY',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User does not have enough money to buy stock.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
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

	timestamp = round(time.time() * 1000)
	
	if (result['success'] == 1):
		logInput = {
			'action': 'remove',
			'userid': userid,
			'amount': amount
		}
		logType = 'AccountTransactionType'
		logfile += log_data(logInput,timestamp,logType)
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
	global logfile

	foundUser = get_user_from_db(userid)
	
	timestamp = round(time.time() * 1000)

	if (foundUser == None):
		logInput = {
			'command': 'COMMIT_BUY',
			'userid': userid,
			'error':  'User does not exist in DB.'
		}
		logType = 'ErrorEventType_1'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (foundUser['pending_buy'] == None):
		logInput = {
			'command': 'COMMIT_BUY',
			'userid': userid,
			'error':  'User does not have a pending buy.'
		}
		logType = 'ErrorEventType_1'
		logfile += log_data(logInput,timestamp,logType)
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
	global logfile

	foundUser = get_user_from_db(userid)
	
	timestamp = round(time.time() * 1000)

	if (foundUser == None):
		logInput = {
			'command': 'CANCEL_BUY',
			'userid': userid,
			'error':  'User does not exist in DB.'
		}
		logType = 'ErrorEventType_1'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (foundUser['pending_buy'] == None):
		logInput = {
			'command': 'CANCEL_BUY',
			'userid': userid,
			'error':  'User has no buy pending so nothing happened.'
		}
		logType = 'ErrorEventType_1'
		logfile += log_data(logInput,timestamp,logType)
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
	global logfile

	foundUser = get_user_from_db(userid)
	
	timestamp = round(time.time() * 1000)

	if (foundUser == None):
		logInput = {
			'command': 'SELL',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User does not exist in DB.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (stock not in foundUser['stocks']):
		logInput = {
			'command': 'SELL',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User does not have the stock to sell.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
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

	timestamp = round(time.time() * 1000)

	if (result['success'] == 1):
		logInput = {
			'action': 'add',
			'userid': userid,
			'amount': sell_price
		}
		logType = 'AccountTransactionType'
		logfile += log_data(logInput,timestamp,logType)
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
	global logfile

	foundUser = get_user_from_db(userid)
	
	timestamp = round(time.time() * 1000)

	if (foundUser == None):
		logInput = {
			'command': 'COMMIT_SELL',
			'userid': userid,
			'error':  'User does not exist in DB.'
		}
		logType = 'ErrorEventType_1'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (foundUser['pending_sell'] == None):
		logInput = {
			'command': 'COMMIT_SELL',
			'userid': userid,
			'error':  'User does not have a pending sell.'
		}
		logType = 'ErrorEventType_1'
		logfile += log_data(logInput,timestamp,logType)
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
		
		if (foundUser['stocks'][stock]['units'] < 1):
			# user has no more of this stock so we will remove it from their stock list
			del foundUser['stocks'][stock]
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
	global logfile

	foundUser = get_user_from_db(userid)
	
	timestamp = round(time.time() * 1000)

	if (foundUser == None):
		logInput = {
			'command': 'CANCEL_SELL',
			'userid': userid,
			'error':  'User does not exist in DB.'
		}
		logType = 'ErrorEventType_1'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (foundUser['pending_sell'] == None):
		logInput = {
			'command': 'CANCEL_SELL',
			'userid': userid,
			'error':  'User has no sell pending so nothing happened.'
		}
		logType = 'ErrorEventType_1'
		logfile += log_data(logInput,timestamp,logType)
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
	global logfile

	foundUser = get_user_from_db(userid)

	timestamp = round(time.time() * 1000)

	if (foundUser == None):
		logInput = {
			'command': 'SET_BUY_AMOUNT',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User does not exist in DB.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (foundUser['cash'] < amount):
		logInput = {
			'command': 'SET_BUY_AMOUNT',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User needs to add more money.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User does not have enough moeny in their account.',
			'error': 'User needs to add more money.'
		}
		
	# user has enough money in their account so now we deduct the money 
	foundUser['cash'] -= amount
	
	# check if the user already has a buy trigger for this stock
	
	if (stock in foundUser['buy_triggers']):
		# put the money from the previous order back into the user's account so that we can make the new order
		foundUser['cash'] += foundUser['buy_triggers'][stock]['total_cash']
	
	# setup the buy_trigger
	foundUser['buy_triggers'][stock] = {
		'unit_price': None,
		'total_cash': amount,
		'active': 0
	}
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
		return {
			'success': 1,
			'message': f'Set buy amount confirmed, but still need to set buy trigger.',
			'result': result['user']
		}
	
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': get_user_from_db(userid),
		'error': result['error']
	}

def handle_set_buy_trigger(userid, stock, amount):
	global logfile
	
	foundUser = get_user_from_db(userid)

	timestamp = round(time.time() * 1000)

	if (foundUser == None):
		logInput = {
			'command': 'SET_BUY_TRIGGER',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User does not exist in DB.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (stock not in foundUser['buy_triggers']):
		logInput = {
			'command': 'SET_BUY_TRIGGER',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User must execute a set_buy_amount for the stock first.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User does not yet have a buy amount set for this stock.',
			'error': 'User must execute a set_buy_amount for the stock first.',
			'result': foundUser
		}
		
	if (foundUser['buy_triggers'][stock]['total_cash'] < amount):
		logInput = {
			'command': 'SET_BUY_TRIGGER',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'Not enough cash in the buy trigger to afford 1 stock at this price.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'Cash committed to the buy cannot be less than the buy trigger.',
			'error': 'Not enough cash in the buy trigger to afford 1 stock at this price.',
			'result': foundUser
		}
		
	foundUser['buy_triggers'][stock]['unit_price'] = amount
	foundUser['buy_triggers'][stock]['active'] = 1
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
                monitor_url = 'http://monitor_server:5000/addToBuyList'
                payload = {
                        'stock':stock,
                        'userid':userid,
                        'trigger':amount
                        }
                s = requests.Session()
                s.post(monitor_url, json = payload)
                
                return {
			'success': 1,
			'message': f'Set buy trigger confirmed.',
			'result': result['user']
		}
	
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': get_user_from_db(userid),
		'error': result['error']
	}

def handle_cancel_set_buy(userid, stock):
	global logfile

	foundUser = get_user_from_db(userid)
	
	timestamp = round(time.time() * 1000)

	if (foundUser == None):
		logInput = {
			'command': 'CANCEL_SET_BUY',
			'userid': userid,
			'stock': stock,
			'error':  'User does not exist in DB.'
		}
		logType = 'ErrorEventType_3'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (stock not in foundUser['buy_triggers']):
		logInput = {
			'command': 'CANCEL_SET_BUY',
			'userid': userid,
			'stock': stock,
			'error':  'User does not currently have a pending buy for this stock so nothing happened.'
		}
		logType = 'ErrorEventType_3'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 1,
			'message': 'User does not currently have a pending buy for this stock so nothing happened.',
			'result': foundUser
		}
		
	foundUser['cash'] += foundUser['buy_triggers'][stock]['total_cash']
	
	del foundUser['buy_triggers'][stock]
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):

		monitor_url = 'http://monitor_server:5000/cancelBuy'
		payload = {
			'stock': stock,
			'userid': userid
			}
		s = requests.Session()
		s.post(monitor_url, json = payload)
				
		return {
			'success': 1,
			'message': f'Set buy trigger cancelled and money has been added back to the user\'s account.',
			'result': result['user']
		}
	
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': get_user_from_db(userid),
		'error': result['error']
	}

def handle_set_sell_amount(userid, stock, amount):
	global logfile
	
	foundUser = get_user_from_db(userid)
	
	timestamp = round(time.time() * 1000)

	if (foundUser == None):
		logInput = {
			'command': 'SET_SELL_AMOUNT',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User does not exist in DB.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (stock not in foundUser['stocks']):
		logInput = {
			'command': 'SET_SELL_AMOUNT',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User does not own any of this stock yet.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User does not currently own any of that stock.',
			'error': 'User doesn\'t own this stock yet.',
			'result': foundUser
		}
		
	if (foundUser['stocks'][stock]['units'] < amount):
		logInput = {
			'command': 'SET_SELL_AMOUNT',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User does not own enough of this stock.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User does not currently own enough of the stock.',
			'error': 'User doesn\'t own enough of this stock.',
			'result': foundUser
		}
		
	if (stock in foundUser['sell_triggers']):
		# there is already a sell trigger for this stock so we will overwrite it
		if (foundUser['sell_triggers'][stock]['active']):
			# the trigger is active which means the stocks have already been deducted from the user's account
			# so first, we need to put those stocks back into their account
			foundUser['stocks'][stock]['units'] += foundUser['sell_triggers'][stock]['units']
			foundUser['stocks'][stock]['cost'] += foundUser['sell_triggers'][stock]['units'] * foundUser['sell_triggers'][stock]['unit_price']
	
	foundUser['sell_triggers'][stock] = {
		'unit_price': None,
		'units': amount,
		'active': 0
	}
			
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
		return {
			'success': 1,
			'message': f'Set sell amount confirmed, but still need to set sell trigger.',
			'result': result['user']
		}
	
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': get_user_from_db(userid),
		'error': result['error']
	}

def handle_set_sell_trigger(userid, stock, amount):
	global logfile
	
	foundUser = get_user_from_db(userid)
	
	timestamp = round(time.time() * 1000)

	if (foundUser == None):
		logInput = {
			'command': 'SET_SELL_TRIGGER',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User does not exist in DB.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (stock not in foundUser['sell_triggers']):
		logInput = {
			'command': 'SET_SELL_TRIGGER',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User must execute a set_sell_amount for this stock first.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User has not yet created a pending sell for this stock.',
			'error': 'User must execute a set_sell_amount for this stock first.',
			'result': foundUser
		}
		
	if (stock not in foundUser['stocks']):
		logInput = {
			'command': 'SET_SELL_TRIGGER',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User must have sold the stock after setting the sell amount.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User doesn\'t currently own any of that stock.',
			'error': 'User must have sold the stock after setting the sell amount.',
			'result': foundUser
		}
		
	if (foundUser['stocks'][stock]['units'] < foundUser['sell_triggers'][stock]['units']):
		logInput = {
			'command': 'SET_SELL_TRIGGER',
			'userid': userid,
			'stock': stock,
			'amount': amount,
			'error':  'User must have sold some of the stock after setting the sell amount.'
		}
		logType = 'ErrorEventType_4'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User doesn\'t currently own enough of the stock. Try a new set_sell_amount.',
			'error': 'User must have sold some of the stock after setting the sell amount.',
			'result': foundUser
		}
		
	foundUser['stocks'][stock]['units'] -= foundUser['sell_triggers'][stock]['units']
	foundUser['stocks'][stock]['cost'] -= amount * foundUser['sell_triggers'][stock]['units']
	
	if (foundUser['stocks'][stock]['units'] < 1):
		# user has no more of this stock so we will remove it from their list
		del foundUser['stocks'][stock]
		
	foundUser['sell_triggers'][stock]['unit_price'] = amount
	foundUser['sell_triggers'][stock]['active'] = 1
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
		print("ATTEMPTING TO ADD TO MONITOR SERVER SELL LIST", flush=True)
		monitor_url = 'http://monitor_server:5000/addToSellList'
		payload = {
                	'stock':stock,
                	'userid':userid,
                	'trigger':amount
			}
		s = requests.Session()
		s.post(monitor_url, json = payload)

		return {
			'success': 1,
			'message': f'Set sell trigger confirmed.',
			'result': result['user']
		}
	
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': get_user_from_db(userid),
		'error': result['error']
	}
		

def handle_cancel_set_sell(userid, stock):
	global logfile
	
	foundUser = get_user_from_db(userid)

	timestamp = round(time.time() * 1000)

	if (foundUser == None):
		logInput = {
			'command': 'CANCEL_SET_SELL',
			'userid': userid,
			'stock': stock,
			'error':  'User does not exist in DB.'
		}
		logType = 'ErrorEventType_3'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
		
	if (stock not in foundUser['sell_triggers']):
		logInput = {
			'command': 'CANCEL_SET_SELL',
			'userid': userid,
			'stock': stock,
			'error':  'User does not currently have a pending sell for this stock so nothing happened.'
		}
		logType = 'ErrorEventType_3'
		logfile += log_data(logInput,timestamp,logType)
		return {
			'success': 1,
			'message': 'User does not currently have a pending sell for this stock so nothing happened.',
			'result': foundUser
		}
	
	if (foundUser['sell_triggers'][stock]['active'] == 1):
		# sell trigger is active so we need to add the stock units back to the user's account
		if (stock not in foundUser['stocks']):
			# stock no longer exists in their account so we need to create it again
			foundUser['stocks'][stock] = {
				'units': foundUser['sell_triggers'][stock]['units'],
				'cost': foundUser['sell_triggers'][stock]['units'] * foundUser['sell_triggers'][stock]['unit_price']
			}
		else:
			foundUser['stocks'][stock]['units'] += foundUser['sell_triggers'][stock]['units']
			foundUser['stocks'][stock]['cost'] += foundUser['sell_triggers'][stock]['units'] * foundUser['sell_triggers'][stock]['unit_price']
	
	del foundUser['sell_triggers'][stock]
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
		
		monitor_url = 'http://monitor_server:5000/cancelSell'
		payload = {
			'stock': stock,
			'userid': userid
			}
		s = requests.Session()
		s.post(monitor_url, json = payload)

		return {
			'success': 1,
			'message': f'Set sell trigger cancelled and stock units have been added back to the user\'s account.',
			'result': result['user']
		}
	
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': get_user_from_db(userid),
		'error': result['error']
	}

def handle_display_summary(userid):
	return {'success': 1, 'message': 'This is the display_summary command.'}

def handle_dumplog():
	global logfile
	global transactionNum
	logs = logfile + '</log>\n'
	transactionNum = 0
	logfile = '<?xml version=\"1.0\"?>\n<log>\n'
	return {
		'success': 1, 
		'message': 'This is the dumplog command.',
		'result': logs
	}
	
def handle_execute_buy_trigger(userid, stock, unit_price):
	# this function is called when the monitor server detects a stock price is 
	# within a trigger limit so we can now execute that trigger at the given price
	foundUser = get_user_from_db(userid)
	
	if (foundUser == None):
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
	if (stock not in foundUser['buy_triggers']):
		return {
			'success': 0,
			'message': 'Trigger execution unsuccessful. User does not have a buy trigger for this stock.',
			'result': foundUser,
			'error': 'User does not have a buy trigger for this stock.'
		}	
	if (foundUser['buy_triggers'][stock] == None):
		return {
			'success': 0,
			'message': 'Trigger execution unsuccessful. User does not have a buy trigger for this stock.',
			'result': foundUser,
			'error': 'User does not have a buy trigger for this stock.'
		}
		
	if (foundUser['buy_triggers'][stock]['active'] == 0):
		return {
			'success': 0,
			'message': 'Trigger execution unsuccessful. User\'s buy trigger for this stock is not currently active.',
			'result': foundUser,
			'error': 'Buy trigger inactive.'
		}
		
	num_units = int(foundUser['buy_triggers'][stock]['total_cash'] / unit_price)
	cost = round(num_units * unit_price, 2)
	leftover_cash = foundUser['buy_triggers'][stock]['total_cash'] - cost
	
	# add the leftover_cash back to the user's account,
	# add num_units of stock to the user's account,
	# remove the buy trigger from the user's account
	
	foundUser['cash'] += leftover_cash
	foundUser['cash'] = round(foundUser['cash'], 2)
		
	if stock in foundUser['stocks']:
		# user already has this stock so we just add the values together
		foundUser['stocks'][stock]['units'] += num_units
		foundUser['stocks'][stock]['cost'] += cost
		foundUser['stocks'][stock]['cost'] = round(foundUser['stocks'][stock]['cost'], 2)
	else:
		# stock doesn't exist yet so we add a new entry
		foundUser['stocks'][stock] = {
			'units': num_units,
			'cost': cost
		}
		
	del foundUser['buy_triggers'][stock]
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
		return {
			'success': 1,
			'message': f'Buy trigger executed.',
			'result': { 'userid': userid, 'stock': stock }
		}
	
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': { 'userid': userid, 'stock': stock },
		'error': result['error']
	}
	
def handle_execute_sell_trigger(userid, stock, unit_price):
	# this function is called when the monitor server detects a stock price is 
	# within a trigger limit so we can now execute that trigger at the given price
	foundUser = get_user_from_db(userid)
	
	if (foundUser == None):
		return {
			'success': 0,
			'message': 'User has not added any money to their account yet.',
			'error': 'User does not exist in DB.'
		}
	if (stock not in foundUser['sell_triggers']):
		return {
			'success': 0,
			'message': 'Trigger execution unsuccessful. User does not have a buy trigger for this stock.',
			'result': foundUser,
			'error': 'User does not have a sell trigger for this stock.'
		}	
	if (foundUser['sell_triggers'][stock] == None):
		return {
			'success': 0,
			'message': 'Commit unsuccessful. User does not have a sell trigger for this stock.',
			'result': foundUser,
			'error': 'User does not have a sell trigger for this stock.'
		}
	
	# calculate how much cash the user will get from the sale
	# add the cash to the user's account
	# delete the stock from their sell triggers
	
	total_price = foundUser['sell_triggers'][stock]['units'] * unit_price
	estimated_price = foundUser['sell_triggers'][stock]['unit_price'] * foundUser['sell_triggers'][stock]['units']
	
	foundUser['cash'] += total_price
		
	if stock in foundUser['stocks']:
		# user still has some of this stock so we can subtract the difference of the sale to the cost
		foundUser['stocks'][stock]['cost'] -= total_price - estimated_price
		
	del foundUser['sell_triggers'][stock]
	
	result = update_user_in_db(foundUser)
	
	if (result['success'] == 1):
		return {
			'success': 1,
			'message': f'Sell trigger executed.',
			'result': { 'userid': userid, 'stock': stock }
		}
	
	return {
		'success': 0,
		'message': 'Database write was unsuccessful',
		'result': { 'userid': userid, 'stock': stock },
		'error': result['error']
	}

def log_data(data, timestamp, logType):
	global transactionNum
	if (logType == 'QuoteServerType'):
		server = 'QSRV'
		return ("\t<quoteServer>\n"
			"\t\t<timestamp>{}</timestamp>\n"
			"\t\t<server>{}</server>\n"
			"\t\t<transactionNum>{}</transactionNum>\n"
			"\t\t<quoteServerTime>{}</quoteServerTime>\n"
			"\t\t<username>{}</username>\n"
			"\t\t<stockSymbol>{}</stockSymbol>\n"
			"\t\t<price>{}</price>\n"
			"\t\t<cryptokey>{}</cryptokey>\n"
			"\t</quoteServer>\n"
			.format(timestamp,
			server,
			transactionNum,
			data['timestamp'],
			data['userid'],
			data['stock'].upper(),
			"{:.2f}".format(data['price']),
			data['hash'].rstrip()))
	elif (logType == 'UserCommandType_0'):
		server = 'CLI'
		return ("\t<userCommand>\n"
			"\t\t<timestamp>{}</timestamp>\n"
			"\t\t<server>{}</server>\n"
			"\t\t<transactionNum>{}</transactionNum>\n"
			"\t\t<command>{}</command>\n"
			"\t\t<filename>{}</filename>\n"
			"\t</userCommand>\n"
			.format(timestamp,
			server,
			transactionNum,
			data['command'].upper(),
			data['filename']))
	elif (logType == 'UserCommandType_1'):
		server = 'CLI'
		return ("\t<userCommand>\n"
			"\t\t<timestamp>{}</timestamp>\n"
			"\t\t<server>{}</server>\n"
			"\t\t<transactionNum>{}</transactionNum>\n"
			"\t\t<command>{}</command>\n"
			"\t\t<username>{}</username>\n"
			"\t</userCommand>\n"
			.format(timestamp,
			server,
			transactionNum,
			data['command'].upper(),
			data['userid']))
	elif (logType == 'UserCommandType_2'):
		server = 'CLI'
		return ("\t<userCommand>\n"
			"\t\t<timestamp>{}</timestamp>\n"
			"\t\t<server>{}</server>\n"
			"\t\t<transactionNum>{}</transactionNum>\n"
			"\t\t<command>{}</command>\n"
			"\t\t<username>{}</username>\n"
			"\t\t<funds>{}</funds>\n"
			"\t</userCommand>\n"
			.format(timestamp,
			server,
			transactionNum,
			data['command'].upper(),
			data['userid'],
			"{:.2f}".format(data['amount'])))
	elif (logType == 'UserCommandType_3'):
		server = 'CLI'
		return ("\t<userCommand>\n"
			"\t\t<timestamp>{}</timestamp>\n"
			"\t\t<server>{}</server>\n"
			"\t\t<transactionNum>{}</transactionNum>\n"
			"\t\t<command>{}</command>\n"
			"\t\t<username>{}</username>\n"
			"\t\t<stockSymbol>{}</stockSymbol>\n"
			"\t</userCommand>\n"
			.format(timestamp,
			server,
			transactionNum,
			data['command'].upper(),
			data['userid'],
			data['stock'].upper()))
	elif (logType == 'UserCommandType_4'):
		server = 'CLI'
		return ("\t<userCommand>\n"
			"\t\t<timestamp>{}</timestamp>\n"
			"\t\t<server>{}</server>\n"
			"\t\t<transactionNum>{}</transactionNum>\n"
			"\t\t<command>{}</command>\n"
			"\t\t<username>{}</username>\n"
			"\t\t<stockSymbol>{}</stockSymbol>\n"
			"\t\t<funds>{}</funds>\n"
			"\t</userCommand>\n"
			.format(timestamp,
			server,
			transactionNum,
			data['command'].upper(),
			data['userid'],
			data['stock'].upper(),
			"{:.2f}".format(data['amount'])))
	elif (logType == 'AccountTransactionType'):
		server = 'TSRV'
		return ("\t<accountTransaction>\n"
			"\t\t<timestamp>{}</timestamp>\n"
			"\t\t<server>{}</server>\n"
			"\t\t<transactionNum>{}</transactionNum>\n"
			"\t\t<action>{}</action>\n"
			"\t\t<username>{}</username>\n"
			"\t\t<funds>{}</funds>\n"
			"\t</accountTransaction>\n"
			.format(timestamp,
			server,
			transactionNum,
			data['action'],
			data['userid'],
			"{:.2f}".format(data['amount'])))
	elif (logType == 'ErrorEventType_1'):
		server = 'TSRV'
		return ("\t<errorEvent>\n"
			"\t\t<timestamp>{}</timestamp>\n"
			"\t\t<server>{}</server>\n"
			"\t\t<transactionNum>{}</transactionNum>\n"
			"\t\t<command>{}</command>\n"
			"\t\t<username>{}</username>\n"
			"\t\t<errorMessage>{}</errorMessage>\n"
			"\t</errorEvent>\n"
			.format(timestamp,
			server,
			transactionNum,
			data['command'].upper(),
			data['userid'],
			data['error']))
	elif (logType == 'ErrorEventType_2'):
		server = 'TSRV'
		return ("\t<errorEvent>\n"
			"\t\t<timestamp>{}</timestamp>\n"
			"\t\t<server>{}</server>\n"
			"\t\t<transactionNum>{}</transactionNum>\n"
			"\t\t<command>{}</command>\n"
			"\t\t<username>{}</username>\n"
			"\t\t<funds>{}</funds>\n"
			"\t\t<errorMessage>{}</errorMessage>\n"
			"\t</errorEvent>\n"
			.format(timestamp,
			server,
			transactionNum,
			data['command'].upper(),
			data['userid'],
			"{:.2f}".format(data['amount']),
			data['error']))
	elif (logType == 'ErrorEventType_3'):
		server = 'TSRV'
		return ("\t<errorEvent>\n"
			"\t\t<timestamp>{}</timestamp>\n"
			"\t\t<server>{}</server>\n"
			"\t\t<transactionNum>{}</transactionNum>\n"
			"\t\t<command>{}</command>\n"
			"\t\t<username>{}</username>\n"
			"\t\t<stockSymbol>{}</stockSymbol>\n"
			"\t\t<errorMessage>{}</errorMessage>\n"
			"\t</errorEvent>\n"
			.format(timestamp,
			server,
			transactionNum,
			data['command'].upper(),
			data['userid'],
			data['stock'].upper(),
			data['error']))
	elif (logType == 'ErrorEventType_4'):
		server = 'TSRV'
		return ("\t<errorEvent>\n"
			"\t\t<timestamp>{}</timestamp>\n"
			"\t\t<server>{}</server>\n"
			"\t\t<transactionNum>{}</transactionNum>\n"
			"\t\t<command>{}</command>\n"
			"\t\t<username>{}</username>\n"
			"\t\t<stockSymbol>{}</stockSymbol>\n"
			"\t\t<funds>{}</funds>\n"
			"\t\t<errorMessage>{}</errorMessage>\n"
			"\t</errorEvent>\n"
			.format(timestamp,
			server,
			transactionNum,
			data['command'].upper(),
			data['userid'],
			data['stock'].upper(),
			"{:.2f}".format(data['amount']),
			data['error']))
	
def create_user(userid):
	'''
	Example user:
	{
		'username': "charles",
		'cash': 75.0,
		'stocks': {
			'ABC': {
				'cost': 29.80			# total amount of cash spent on these stocks. (just a stat for curiosity)
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
		'buy_triggers' = {				# we assume that each stock can only have 1 buy trigger active
			'ABC': {					# so if we tried to add another buy trigger for ABC, it would overwrite the current one
				'unit_price': 20.50,
				'total_cash': 61.50,	# this amount has already been deducted from their 'cash' amount
				'active': 1
			},
		}
		'sell_triggers' = {				# im not sure if we should remove the stock units from the 'stocks' attribute when a sell_trigger is created
			'ABC': {	
				'unit_price': None,		# value specified in set_buy_trigger
				'units': 5,				# value specified in set_buy_amount. the number of stocks that are to be sold. stocks aren't deducted from user's account until the unit_price (set_buy_trigger) has been set
				'active': 0
			},
		}
	}
	'''
	return {
		'username': userid,
		'cash': 0.0,
		'pending_buy': None,
		'pending_sell': None,
		'stocks': {},
		'buy_triggers': {},
		'sell_triggers': {}
	}
	
def create_quote(stock, price, userid, timestamp, hash):
	'''
	Example quote:
	{
		"stock": 'ABC',
		"price": 12.55,
		"userid": userid,						# the user who generated the original quote
		"timestamp": 1612739531162,				# time returned from the quote server
		"hash": 'xAnC1CbuaY6ndlIENDMVXbWxCMpm2x4wdZMbaxgvIHE=\n',
		"docker_timestamp": 1289753985			# the time on the local server used for staleness checks
	}
	'''
	return {
		'stock': stock,
		'price': price,
		'userid': userid,
		'timestamp': timestamp,
		'hash': hash,
		'docker_timestamp': int(time.time())
	}

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)

