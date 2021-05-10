## Installation

```
pip install -U -r requirements.txt
```
## System Architecture
The system consists of three microservices:

* require_rand
* primary rand_server
* secondary rand_server

### require_rand service
This application acts as the interface for the user to interact with the system. The user can send a positive integer value to the require_rand service which will in turn send a request to a rand_server which will return a randomly generated integer between 0 and the given value. require_rand will then print the result to the user together with the information about which server (primary or secondary) that calculated the number.

### primary rand_server
Listens for post-requests that contains a positive integer value and returns a random number between 0 and the given value. Will return an error message if the value is not valid (not a number, out of range, etc.).
In this demo the primary server must use port 8002 and be named "primary".

### secondary rand_server
The secondary rand_server is identically to the primary one. The difference is that the require_rand service will try to request the value from the primary server first. In this demo the secondary server must use port 8003 and be named "secondary".

## Start our Microservices

Start service 1:
```
python require_rand.py
```
Start service 2 in a seperate terminal:
```
python rand_server.py 8002 "primary"
```
Start service 3 in a seperate terminal:
```
python rand_server.py 8003 "secondary"
```

To test that the services work perform a simple call:
```
curl -k http://localhost:8001/index/10
> response from service: 5
```

## Chaos Testing Experiment
Tests in Chaos Toolkit are called Experiments. Experiments build on three phases:

* Steady State Hypothesis
* Method
* Rollbacks

The different stages are built upon Actions and Probes.

### Actions and Probes

* Actions is used to interact with the system.
* Probes is used to query the system.

### Steady State Hypothesis
When the experiment starts it first checks the *Steady State Hypothesis* to assert that our system works as intended. The Steady State is the state we except our system to be in normally. The *Steady State Hypothesis* is asserted using *Probes.*

### Method
Here we interact with the system in some way to test the robustness of the system. In our demo we kill the primary server in this stage to see how the rest of the system reacts. The *Method* is created with *Actions* and *Probes.*

### Rollbacks
After the experiment has been completed it tries to rollback the system to its steady state. The *Rollbacks* are created using *Actions.*

### Order of stages
The experiments run in this order:
1. Steady State Hypothesis
2. Method
3. Steady State Hypothesis 
4. Rollbacks

After the Method stage the experiments checks if the systems still is in the steady state or if our steady state has broken down. The experiment will fail if the Steady State is not valid in either of its steps.




## Run the experiment
To start the experiment first start the three microservices. 
```
chaos run experiment.json
```



## Note
These experiments have been tested and run on:
* Ubuntu                 20.04 LTS
* Python                 3.8.5
* chaostoolkit           1.9.0
* CherryPy               18.6.0
* requests               2.25.1
