Optimization service for modflow and mt3d-usgs models.

Start command: "python ./main.py"

The main.py creates a message consumer that listens to the optimization request queue "REQUEST_QUEUE".
When new optimization task is published, consumer creates worker containers, assigns tasks to them in detached mode and continues consuming.
When the job is finished containers are stopped automatically.

Example input can be found in ./tests.


System recuirements:
- Python version >= 3.5
- Docker version >= 18
- Python libraries: pika, doker

Configuration is defined in the ./config.json file, where:
    
    "HTTP_PROXY" and "HTTPS_PROXY": proxy ports if proxy server is used,
    "HOST_TEMP_FOLDER": folder on the host to which temporary model files will be written,
    "DOCKER_TEMP_FOLDER": folder in the docker containers to which temporary model files will be written,
    "MODEL_FILE_NAME": name of optimization-model input file that will be created,
    "RABBITMQ_HOST": rabbitmq server host,
    "RABBITMQ_PORT": rabbitmq server port,
    "RABBITMQ_VIRTUAL_HOST": rabbitmq server virtual host,
    "RABBITMQ_USER": rabbitmq server username,
    "RABBITMQ_PASSWORD": rabbitmq server password,
    "REQUEST_QUEUE": name of the queue that service is listening to,
    "RESPONSE_QUEUE": name of the queue to which results will be published,
    "SIMULATION_REQUEST_QUEUE": name of the simulation jobs request queue (used only internally, created by the service and deleted after the optimization is finished),
    "SIMULATION_RESPONSE_QUEUE": name of the simulation jobs results queue (used only internally, created by the service and deleted after the optimization is finished),
    "NUM_SOLVERS_GA": number of simulation worker containers that will be created for each new optimization task by default,
    "OPTIMIZATION_IMAGE": name of the optimization docker image (docker file can be found in ./Optimization),
    "SIMULATION_IMAGE": name of the simulation docker image (docker file can be found in ./Simulation)