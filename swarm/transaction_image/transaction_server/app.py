from flask import Flask
from flask import request
from pymongo import MongoClient

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
		
		return { 'success': 'false', 'message': 'Commmand not recognized.' }

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
	result_str = str(random_price) + ',' + stock + ',' + userid + ',1612739531162,xAnC1CbuaY6ndlIENDMVXbWxCMpm2x4wdZMbaxgvIHE=\n'
	result = result_str.encode()
	
	return result.decode("utf-8")
		
def handle_add(userid, amount):
	foundUser = users.find_one({"Username": userid});
	
	if (foundUser == None):
		foundUser = create_user(userid)
	
	foundUser['Cash'] += float(amount)
	
	result = users.replace_one({'Username': userid}, foundUser, True)
	
	if (result.matched_count > 0 or result.upserted_id != None):
		if ('_id' in foundUser):
			del foundUser['_id']
		return {
			'success': 1, 
			'message': 'Successfully added money to the account.',
			'result': foundUser
		}
	
	return {'success': 0, 'message': 'Database update was unsuccessful.'}
	
def handle_quote(userid, stock):
	return {'success': 1, 'message': 'This is the quote command.'}

def handle_buy(userid, stock, amount):
	return {'success': 1, 'message': 'This is the buy command.'}
	
def handle_commit_buy(userid):
	return {'success': 1, 'message': 'This is the commit_buy command.'}

def handle_cancel_buy(userid):
	return {'success': 1, 'message': 'This is the cancel_buy command.'}

def handle_sell(userid, stock, amount):
	return {'success': 1, 'message': 'This is the sell command.'}

def handle_commit_sell(userid):
	return {'success': 1, 'message': 'This is the commit_sell command.'}

def handle_cancel_sell(userid):
	return {'success': 1, 'message': 'This is the cancel_sell command.'}

def handle_set_buy_amount(userid, stock, amount):
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
	return {
		'Username': userid,
		'Cash': 0.0
	}

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)

