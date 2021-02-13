import time
import threading
import json
import random
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

@app.before_first_request
def activate_monitoring():

	def watch_buys():
		while(True):
			if cache.get("BUY_LIST") is None:
				print("watching buys", flush=True)
			#bring BUY_LIST into env, check all stocks (the sharing of the resource means it must be async)
			else:
				buy_list_s = cache.get("BUY_LIST")
				print("BUY_LIST:\n" + buy_list_s, flush=True)
			
			time.sleep(3)

	def watch_sells():
		while(True):
			if cache.get("SELL_LIST") is None:
				print("watching sells", flush=True)
			else:
				sell_list_s = cache.get("SELL_LIST")
				print("SELL_LIST:\n" + sell_list_s, flush=True)
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

	print(request.data, flush=True)
	
	data = request.json
	userid = data['userid']
	stock = data['stock']
	trigger = data['trigger']
	
	if cache.get("BUY_LIST") is None:
		entry = {stock: [(userid, trigger)]}
		cache.set("BUY_LIST", json.dumps(entry))
	else:
		buy_list_s = cache.get("BUY_LIST")
		buy_list = json.loads(buy_list_s)
		if stock in buy_list:
			buy_list[stock].append((userid, trigger))
		else:
			buy_list[stock] = [(userid, trigger)]

		cache.set("BUY_LIST", json.dumps(buy_list))

	return 'added to buy list'

@app.route('/addToSellList', methods=['GET', 'POST'])
def add_sell():
	if request.method=="GET":
		return 'this is the monitor selllist endpoint\n'
	
	print(request.json, flush=True)
	data = request.json
	userid = data['userid']
	stock = data['stock']
	trigger = data['trigger']

	if cache.get("SELL_LIST") is None:
		entry = {stock: [(userid, trigger)]}
		cache.set("SELL_LIST", json.dumps(entry))
	else:
		sell_list_s = cache.get("SELL_LIST")
		sell_list = json.loads(sell_list_s)
		if stock in sell_list:
			sell_list[stock].append((userid, trigger))
		else:
			sell_list[stock] = [(userid, trigger)]

		cache.set("SELL_LIST", json.dumps(sell_list))

	return 'added to sell list'

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)

