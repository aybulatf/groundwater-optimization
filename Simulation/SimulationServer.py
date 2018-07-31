#!/usr/bin/env python

import os
import sys
import pika
import json

from Simulation import Simulation


class SimulationServer(object):

    def __init__(self):

        self.optimization_id = os.environ['OPTIMIZATION_ID']
        self.simulation_request_queue = os.environ['SIMULATION_REQUEST_QUEUE']+\
        self.optimization_id
        
        self.simulation_response_queue = os.environ['SIMULATION_RESPONSE_QUEUE']+\
        self.optimization_id
    
        self.request_consumer_tag = 'simulation_request_consumer'

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.environ['RABBITMQ_HOST'],
                port=int(os.environ['RABBITMQ_PORT']),
                virtual_host=os.environ['RABBITMQ_VIRTUAL_HOST'],
                credentials=pika.PlainCredentials(os.environ['RABBITMQ_USER'], os.environ['RABBITMQ_PASSWORD'])
            )
        )
        self.request_channel = self.connection.channel()
        self.request_channel.queue_declare(
            queue=self.simulation_request_queue,
            durable=True
        )
        self.response_channel = self.connection.channel()
        self.response_channel.queue_declare(
            queue=self.simulation_response_queue,
            durable=True
        )

    def consume(self):
        self.request_channel.basic_consume(
            self.on_request, queue=self.simulation_request_queue,
            consumer_tag=self.request_consumer_tag
        )
        print(" [x] Simulation server awaiting requests")
        self.request_channel.start_consuming()

    def on_request(self, channel, method, properties, body):
        channel.basic_ack(delivery_tag = method.delivery_tag)
        content = json.loads(body.decode("utf-8"))

        if 'time_to_die' in content and content['time_to_die'] == True:
            print(" [-] Stopping simulation server")
            self.request_channel.basic_cancel(consumer_tag=self.request_consumer_tag)
            self.connection.close()
            sys.exit()

        ind_id = content['ind_id']
        objects_data = content['objects_data']
        simulation_id = content['simulation_id']

        try:
            simulation = Simulation(simulation_id=simulation_id)
            fitness = simulation.evaluate(objects_data)
            response = {
                'status_code': '200',
                'ind_id': ind_id,
                'fitness': fitness,
                'message': 'Successfully finished simulation task for optimization: {}, simulation: {}'\
                .format(self.optimization_id, simulation_id),
            }

        except Exception as e:
            print(str(e))
            response = {
                'status_code': '500',
                'ind_id': ind_id,
                'fitness': None,
                'message': str(e),
            }

        response = json.dumps(response).encode()

        print(' [.] Publishing result to the simulation response queue: {}'\
        .format(self.simulation_response_queue))
        self.response_channel.basic_publish(
            exchange='',
            routing_key=self.simulation_response_queue,
            body=response,
            properties=pika.BasicProperties(
                delivery_mode=2  # make message persistent
            )
        )


if __name__ == "__main__":
    ss = SimulationServer()
    ss.connect()
    ss.consume()


