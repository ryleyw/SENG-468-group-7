import time
import threading
import json
import random
import socket
import requests
from pymongo import MongoClient
from flask import Flask
from flask import request
from flask_caching import Cache

# MAKE SURE THIS MATCHES WITH THE ONE IN THE TRANSACTION SERVER
cache_time_limit = 120 	# seconds before a cached stock quote becomes stale

client = MongoClient('mongodb://mongos0:27017')
stocks_db = client.stocks
quotes = stocks_db.quotes

s_sell = requests.Session()
s_buy = requests.Session()

# testing 
buy_cache_count = 0
buy_new_count = 0
buy_total_count = 0
sell_cache_count = 0
sell_new_count = 0
sell_total_count = 0

config = {
	"DEBUG": True,
	"CACHE_TYPE": "simple",
	"CACHE_DEFAULT_TIMEOUT": 0
}

app = Flask(__name__)
app.config.from_mapping(config)
cache=Cache(app)
semOne = threading.Semaphore()
semTwo = threading.Semaphore()

@app.before_first_request
def activate_monitoring():
	t_url = 'http://transaction_server:5000/'
	def watch_buys():
		while(True):
			if cache.get("BUY_LIST") is None:
				print("watching buys", flush=True)
			else:
				buy_list_s = cache.get("BUY_LIST")
				buy_list = json.loads(buy_list_s)
				#print("BUY_LIST:\n" + buy_list_s, flush=True)
				for stock in buy_list.keys():
					watchers = buy_list[stock]

					if len(watchers) > 0:

						first = list(watchers.keys())[0] 
						
						buy_total_count += 1
						
						# first we check the DB to see if we already have a cached value for this quote
						found_fresh = False
						foundQuote = quotes.find_one({'stock': stock})
						data = None
						if (foundQuote):
							# check to see if it's stale
							diff = time.time() - foundQuote['docker_timestamp']
							if (diff < cache_time_limit):
								# quote is fresh so we can use it
								found_fresh = True
								
								buy_cache_count += 1
								
								data = {
									'price': foundQuote['price'],
									'stock': foundQuote['stock'],
									'userid': foundQuote['userid'],
									'timestamp': foundQuote['timestamp'],
									'hash': foundQuote['hash']
								}
						if (found_fresh == False):
							# don't have a valid cached value for this stock so we must make a quote request
							skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							skt.connect(('192.168.4.2', 4444))
							msg = f'{stock},{first}\n'
							skt.send(msg.encode())
							result = None
							try:
								result = skt.recv(1024)
							except:
								print('error from quoteserver', flush=True)

							skt.close()
							
							if (result is not None):
								result_str = result.decode('utf-8')
								quote = result_str.split(',')
								data = {
									'price': float(quote[0]),
									'stock':quote[1],
									'userid':quote[2],
									'timestamp':quote[3],
									'hash':quote[4]
								}
								
								buy_new_count += 1
								
								newQuote = create_quote(data['stock'], data['price'], data['userid'], data['timestamp'], data['hash'])
								quotes.replace_one({'stock': data['stock']}, newQuote, True)

						for user in watchers:	
							if data is not None:
								if data['price'] <= float(watchers[user]):

									payload = {
										'command': 'execute_buy_trigger',
										'userid': user,
										'stock': data['stock'],
										'unit_price': data['price']
									}
									r = s_buy.post(t_url, json=payload)

									if r is not None:
										rj = {}
										try:
											rj = r.json()
										except:
											print("error in json decoding")

										if 'success' in rj and rj['success'] == 1:

											semOne.acquire()
											buy_list_s = cache.get("BUY_LIST")
											buy_list = json.loads(buy_list_s)
											if stock in buy_list and user in buy_list[stock]:
												buy_list[stock].pop(user, None)
												cache.set("BUY_LIST", json.dumps(buy_list))
											semOne.release()
									
			time.sleep(1)

	def watch_sells():
		while(True):
			if cache.get("SELL_LIST") is None:
				print("watching sells", flush=True)
			else:
				sell_list_s = cache.get("SELL_LIST")
				sell_list = json.loads(sell_list_s)
				#print("SELL LIST:\n" + sell_list_s, flush=True)
				for stock in sell_list.keys():
					watchers = sell_list[stock]

					if len(watchers) > 0:
						first = list(watchers.keys())[0] 
						
						sell_total_count += 1
						
						# first we check the DB to see if we already have a cached value for this quote
						found_fresh = False
						foundQuote = quotes.find_one({'stock': stock})
						data = None
						if (foundQuote):
							# check to see if it's stale
							diff = time.time() - foundQuote['docker_timestamp']
							if (diff < cache_time_limit):
								# quote is fresh so we can use it
								found_fresh = True
								sell_cache_count += 1
								
								data = {
									'price': foundQuote['price'],
									'stock': foundQuote['stock'],
									'userid': foundQuote['userid'],
									'timestamp': foundQuote['timestamp'],
									'hash': foundQuote['hash']
								}
						if (found_fresh == False):
							# don't have a valid cached value for this stock so we must make a quote request
							skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							skt.connect(('192.168.4.2', 4444))
							msg = f'{stock},{first}\n'
							skt.send(msg.encode())
							result = None
							try:
								result = skt.recv(1024)
							except:
								print('error from quoteserver', flush=True)

							skt.close()
							
							sell_new_count += 1
							
							if (result is not None):
								result_str = result.decode('utf-8')
								quote = result_str.split(',')
								data = {
									'price': float(quote[0]),
									'stock':quote[1],
									'userid':quote[2],
									'timestamp':quote[3],
									'hash':quote[4]
								}
								
								newQuote = create_quote(data['stock'], data['price'], data['userid'], data['timestamp'], data['hash'])
								quotes.replace_one({'stock': data['stock']}, newQuote, True)
								
						for user in watchers:	
							if data is not None:								
								if data['price'] >= float(watchers[user]):

									payload = {
										'command': 'execute_sell_trigger',
										'userid': user,
										'stock': data['stock'],
										'unit_price': data['price']
									}
									
									r = s_sell.post(t_url, json=payload)

									if r is not None:
										rj = {}
										try:
											rj = r.json()
										except:
											print("error in json decoding")
									
										if 'success' in rj and rj['success'] == 1:

											semTwo.acquire()
											sell_list_s = cache.get("SELL_LIST")
											sell_list = json.loads(sell_list_s)
											if stock in sell_list and user in sell_list[stock]:
												sell_list[stock].pop(user, None)
												cache.set("SELL_LIST", json.dumps(sell_list))
											semTwo.release()
									
			time.sleep(1)

	buyThread = threading.Thread(target=watch_buys)
	sellThread = threading.Thread(target=watch_sells)
	buyThread.start()
	sellThread.start()

@app.route('/addToBuyList', methods=['GET', 'POST'])
def add_buy():
	if request.method=="GET":
        	return 'this is the monitor buylist endpoint :)\n'
	
	data = request.json
	userid = data['userid']
	stock = data['stock']
	trigger = data['trigger']

	semOne.acquire()
	if cache.get("BUY_LIST") is None:
		entry = {stock: {userid: trigger}}
		cache.set("BUY_LIST", json.dumps(entry))
	else:
		buy_list_s = cache.get("BUY_LIST")
		buy_list = json.loads(buy_list_s)
		if stock in buy_list:
			buy_list[stock][userid] = trigger
		else:
			buy_list[stock] = {userid: trigger}

		cache.set("BUY_LIST", json.dumps(buy_list))
	semOne.release()
	return 'added to buy list'

@app.route('/cancelBuy', methods=['GET', 'POST'])
def cancel_buy():
	if request.method=='GET':
		return 'this is the cacnel buy :)'
	
	data = request.json
	userid = data['userid']
	stock = data['stock']
	
	
	if cache.get("BUY_LIST") is None:
		return 'User to cancel not found'
	else:   
		semOne.acquire()
		buy_list_s = cache.get("BUY_LIST")
		buy_list = json.loads(buy_list_s)
	
		if stock not in buy_list:
			semOne.release()
			return 'no such trigger'
		
		if userid in buy_list[stock]:
			buy_list[stock].pop(userid, None)
			cache.set("BUY_LIST", json.dumps(buy_list))
			semOne.release()
			return 'stock deleted'
		else:
			semOne.release()
			return 'stock not found'

@app.route('/addToSellList', methods=['GET', 'POST'])
def add_sell():
	if request.method=="GET":
		return 'this is the monitor selllist endpoint\n'
	
	data = request.json
	userid = data['userid']
	stock = data['stock']
	trigger = data['trigger']

	semTwo.acquire()
	if cache.get("SELL_LIST") is None:
		entry = {stock: {userid: trigger}}
		cache.set("SELL_LIST", json.dumps(entry))
	else:
		sell_list_s = cache.get("SELL_LIST")
		sell_list = json.loads(sell_list_s)
		if stock in sell_list:
			sell_list[stock][userid] = trigger
		else:
			sell_list[stock] = {userid: trigger}

		cache.set("SELL_LIST", json.dumps(sell_list))
	semTwo.release()
	return 'added to sell list'

@app.route('/cancelSell', methods=['GET', 'POST'])
def cancel_sell():
	if request.method=='GET':
		return 'this is the cacnel sell :)'
	
	data = request.json
	userid = data['userid']
	stock = data['stock']
	
	if cache.get("SELL_LIST") is None:
		return 'User to cancel not found'
	else:
		semTwo.acquire()
		sell_list_s = cache.get("SELL_LIST")
		sell_list = json.loads(sell_list_s)

		if stock not in sell_list:
			semTwo.release()
			return 'no such trigger'

		if userid in sell_list[stock]:
			sell_list[stock].pop(userid, None)
			cache.set("SELL_LIST", json.dumps(sell_list))
			semTwo.release()			
			return 'stock deleted'
		else:
			semTwo.release()
			return 'stock not found'
			
			
@app.route('/', methods=['GET', 'POST'])
def handle_root():
	if (request.method == 'GET'):
		return 'This is the monitor server (running on python with flask).\n'
		
	elif (request.method == 'POST'):
		data = request.json
		
		if ('command' in data): 
			command = data['command'].lower()
		else: 
			return { 
				'success': 0, 
				'message': 'Must include a command parameter for the post request.',
				'error': 'Must include a command parameter for the post request.'
			}
		
		if (command == 'get_info'):
			return {
				'buy_cache_count': buy_cache_count,
				'buy_new_count':  buy_new_count,
				'buy_total_count': buy_total_count,
				'sell_cache_count': sell_cache_count,
				'sell_new_count': sell_new_count,
				'sell_total_count': sell_total_count 
			}
			
		return { 
			'success': 0, 
			'message': 'Commmand not recognized.',
			'error': 'Command not recognized.'
		}

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)

