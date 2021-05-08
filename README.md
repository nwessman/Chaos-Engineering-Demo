## Installation

```
pip install -U -r requirements.txt
```

## Start our Microservices

Start service 1:
```
python microservice1.py
```
Start service 2 in a seperate terminal:
```
python microservice2.py
```

To test that the services work perform a simple call:
```
curl -k http://localhost:8001/index/10
> response from service: 5
```


## Run the experiment
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
