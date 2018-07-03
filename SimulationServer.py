#!/usr/bin/env python

import os
import sys
import pika
import warnings
import json
import time

from Simulation import Simulation


DATA_FOLDER = os.environ['DATA_FOLDER']
HOST = os.environ['HOST']
PORT = os.environ['PORT']
VIRTUAL_HOST = os.environ['VIRTUAL_HOST']
USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
REQUEST_QUEUE = os.environ['REQUEST_QUEUE']
RESPONSE_QUEUE = os.environ['RESPONSE_QUEUE']

warnings.filterwarnings("ignore")
CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=HOST,
        port=int(PORT),
        virtual_host=VIRTUAL_HOST,
        credentials=pika.PlainCredentials(USER, PASSWORD)
    )
)

def on_request(ch, method, props, body):

    content = json.loads(body.decode("utf-8"))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # content = json.loads(content)
    simulation_id = content['simulation_id']
    optimization_id = content['optimization_id']
    ind_id = content['ind_id']
    objects_data = content['objects_data']

    start = time.time()
    simulation = Simulation(
        data_folder = DATA_FOLDER,
        optimization_id = optimization_id,
        simulation_id = simulation_id
    )
    try:
        fitness = simulation.evaluate(objects_data)
        response = {
            'status_code': '200',
            'ind_id': ind_id,
            'fitness': fitness,
            'message': 'Successfully finished simulation task for optimization: {}, simulation: {}'\
            .format(str(optimization_id), str(simulation_id)),
            'execution_time': time.time() - start
        }

    except Exception as e:
        response = {
            'status_code': '500',
            'ind_id': ind_id,
            'fitness': None,
            'message': str(e),
            'execution_time': time.time() - start
        }

    response = json.dumps(response).encode()

    response_channel.queue_declare(
        queue=RESPONSE_QUEUE + optimization_id,
        durable=True
    )
    print('Publishing result to the simulation response queue: {}'.format(RESPONSE_QUEUE + optimization_id))
    response_channel.basic_publish(
        exchange='',
        routing_key=RESPONSE_QUEUE + optimization_id,
        body=response,
        properties=pika.BasicProperties(
            delivery_mode=2  # make message persistent
        )
    )


if __name__ == "__main__":
    
    request_channel = CONNECTION.channel()
    response_channel = CONNECTION.channel()
    request_channel.queue_declare(
        queue=REQUEST_QUEUE,
        durable=True,
        auto_delete=False
    )
    # request_channel.basic_qos(prefetch_count=1)
    request_channel.basic_consume(on_request, queue=REQUEST_QUEUE)

    print(" [x] Simulation server awaiting requests")
    request_channel.start_consuming()


