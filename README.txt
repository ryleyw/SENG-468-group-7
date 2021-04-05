# SENG-468-group-7

The main files for our project can be found in the /swarm/ folder.

To run the swarm, navigate to the /swarm/ folder and execute the ./restart.sh script.
	(You will need to use sudo for this script on the lab VMs.)
	
This script will start up the swarm with all of the containers and services.

Adding more workers to the swarm within the VMs requires some extra steps that wouldn't be necessary under a normal environment so I won't describe them here.

To access the frontend, you can open your browser within the VM and go to localhost:83.

The API can be reached at localhost:80.

The transaction server can be reached at localhost:81.

The monitor server can be reached at localhost:82.

However, the frontend is the only service that will actually be useful to open within the browser.

To run a workload through the system, open up the workload.py file (within the swarm folder) and modify the workload_filename string at the top of the file based on which workload you want to run.

Then run >python workload.py  (you may need to use the python3 command instead of python).



Explicit example usage:

1) Start the VM.
2) Open a terminal.
3) Type > sudo -s     (All of the docker commands within the scripts require sudo)
4) Enter the password.
5) Navigate to the Desktop (> cd Desktop)
6) > git clone https://github.com/ryleyw/SENG-468-group-7
7) > chmod 777 -R SENG-468-group-7    (so that you can execute the shell script)
8) > cd SENG-468-group-7/swarm/
9) > ./restart.sh                  (to start the swarm and all of its services)
10) You may need to wait up to 10 minutes before all of the services are up and running due to some SSL issues with the VM and uvic firewall.
11) Use your browser or curl to access localhost:80, localhost:81, localhost:82, localhost:83 to make sure all of the services are running.
12) If all of those URLs work immediately, still wait ~5 minutes for the MongoDB cluster to be fully initialized. 
13) > python3 workload.py          (to execute a workload on the system)
14) After the workload is complete, you can find the logfile at /swarm/testLOG.xml. 


If there are any issues getting things setup or run, feel free to contact patrickeholland@gmail.com and I will get back to you ASAP.