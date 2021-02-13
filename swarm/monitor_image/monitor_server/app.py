import time
import threading
import json
import random
import socket
from flask import Flask
from flask import request
from flask_caching import Cache

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
				
				for stock in buy_list.keys():
					watchers = buy_list[stock]
					for user in watchers:
						skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						skt.connect(('192.168.4.2', 4444))
						msg = f'{stock},{user}\n'
						result = None
						try:
							result = skt.recv(1024)
						except:
							print('error from quoteserver', flush=True)
						skt.close()
						if result is not None:
							result_str = result.decode('utf-8')
							quote = result_str.split(',')
							data = {
								'price': float(quote[0]),
								'stock':quote[1],
								'userid':quote[2],
								'timestamp':quote[3],
								'hash':quote[4]
								}
							print("Got stock quote of " + data['stock'] + " with price of " + str(data['price']), flush=True)
			
			time.sleep(3)

	def watch_sells():
		while(True):
			if cache.get("SELL_LIST") is None:
				print("watching sells", flush=True)
			else:
				sell_list_s = cache.get("SELL_LIST")

			#bring SELL_LIST into env, check all stocks 
			time.sleep(4)

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

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)

