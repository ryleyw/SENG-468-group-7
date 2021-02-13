import time
import threading
import json
import random
from flask import Flask
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
				print("watching buys")
			#bring BUY_LIST into env, check all stocks (the sharing of the resource means it must be async)
			else:
				buy_list_s = cache.get("BUY_LIST")
				print(buy_list_s)
			
			time.sleep(3)

	def watch_sells():
		while(True):
			print("watching sells")
			#bring SELL_LIST into env, check all stocks 
			time.sleep(4)

	buyThread = threading.Thread(target=watch_buys)
	sellThread = threading.Thread(target=watch_sells)

	buyThread.start()
	sellThread.start()

@app.route('/addToBuyList', methods=['GET', 'POST'])
def add_request():
	if cache.get("BUY_LIST") is None:
		entry = {"ABC": "AMOUNT"}
		cache.set("BUY_LIST", json.dumps(entry))
	else:
		buy_list_s = cache.get("BUY_LIST")
		buy_list = json.loads(buy_list_s)
		buy_list["XYZ"] = "AMOUNT"
		cache.set("BUY_LIST", json.dumps(buy_list))

	return 'hello world'

@app.route('/removeFromBuyList', methods=['GET', 'POST'])
def remove_request():
	if cache.get("BUY_LIST") is not None:
		buy_list_s = cache.get("BUY_LIST")
		buy_list = json.loads(buy_list_s)
		del buy_list["ABC"]
		cache.set("BUY_LIST", json.dumps(buy_list))
		
	return 'hello world'

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)

