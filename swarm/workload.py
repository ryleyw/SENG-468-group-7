import re
import threading
import json
import requests
import time

workload_filename = "./workloads/workload10.txt"
url = 'http://localhost:80/api/command/' 		# docker swarm web app
#url = 'http://localhost:81'	   				# docker swarm transaction server

users = {}
req_count = {}

def thread_function(userid):
	s = requests.Session()
	command_list = users[userid]
	req_count[userid] = 0
	for data in command_list:
		response = s.post(url, json = data)
		req_count[userid] += 1
		

def main():
	threads = []
	
	i = 0

	start_time = time.time()
	
	with open(workload_filename, "r") as infile:
		for line in infile:
			words = re.split(',|\s', line)
			if (words[1] == 'DUMPLOG'):
				logreq = {
					'command': words[1],
					'filename': words[2]
				}
			else:
				command = words[1]
				userid = words[2]
				
				if (command == 'ADD'):
					req = {
						'command': command,
						'amount': words[3]
					}
				elif (command == 'QUOTE'):
					req = {
						'command': command,
						'stock': words[3]
					}
				elif (command == 'BUY'):
					req = {
						'command': command,
						'stock': words[3],
						'amount': words[4]
					}
				elif (command == 'COMMIT_BUY'):
					req = {
						'command': command
					}
				elif (command == 'CANCEL_BUY'):
					req = {
						'command': command
					}
				elif (command == 'SELL'):
					req = {
						'command': command,
						'stock': words[3],
						'amount': words[4]
					}
				elif (command == 'COMMIT_SELL'):
					req = {
						'command': command
					}
				elif (command == 'CANCEL_SELL'):
					req = {
						'command': command
					}
				elif (command == 'SET_BUY_AMOUNT'):
					req = {
						'command': command,
						'stock': words[3],
						'amount': words[4]
					}
				elif (command == 'SET_BUY_TRIGGER'):
					req = {
						'command': command,
						'stock': words[3],
						'amount': words[4]
					}
				elif (command == 'CANCEL_SET_BUY'):
					req = {
						'command': command,
						'stock': words[3]
					}
				elif (command == 'SET_SELL_AMOUNT'):
					req = {
						'command': command,
						'stock': words[3],
						'amount': words[4]
					}
				elif (command == 'SET_SELL_TRIGGER'):
					req = {
						'command': command,
						'stock': words[3],
						'amount': words[4]
					}
				elif (command == 'CANCEL_SET_SELL'):
					req = {
						'command': command,
						'stock': words[3]
					}
				elif (command == 'DISPLAY_SUMMARY'):
					req = {
						'command': command
					}
				else:
					print(f'command not recognized\n{line}')
					return
				
				req['userid'] = userid
					
				if (userid in users):
					users[userid] += [req]
				else:
					users[userid] = [req]
					
			i += 1
	parse_time = time.time() - start_time
	start_time = time.time()
	print(f'done parsing file. took {parse_time:.4f} seconds')
			
	for user in users:
		t = threading.Thread(target=thread_function, args=(user,))
		threads += [t]
	
	for t in threads:
		t.start()	
		
	for t in threads:
		t.join()
	
	if (logreq):
		response = requests.post(url, logreq)
		obj = json.loads(response.text)
		#if ('data' in obj):
		#	if ('result' in obj['data']):
		#		print(obj['data']['result'])
		f = open(logreq['filename'] + '.xml',"w")
		f.write(obj['data']['result'])
		f.close()
	
	thread_time = time.time() - start_time
	print(f'finished all threads in {thread_time:.4f} seconds')
	# workload 10: 10 threads, 1 of each server: 247.4s
	# changed to requests.Session() -> 209s
	# changed to 10 of each server: 240s



if __name__ == "__main__":
	main()