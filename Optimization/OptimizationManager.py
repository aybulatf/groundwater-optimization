import os
import sys
import pika
import warnings
import json

from Optimization import NSGA, NelderMead

class OptimizationManager(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.environ['RABBITMQ_HOST'],
                port=int(os.environ['RABBITMQ_PORT']),
                virtual_host=os.environ['RABBITMQ_VIRTUAL_HOST'],
                credentials=pika.PlainCredentials(
                    os.environ['RABBITMQ_USER'], os.environ['RABBITMQ_PASSWORD']
                ),
                heartbeat_interval=0
            )
        )
        self.response_channel = self.connection.channel()
        self.response_channel.queue_declare(
            os.environ['RESPONSE_QUEUE'],
            durable=True
        )

    def reply_error(self, exception):
        response = {
            'status_code': "500",
            'solutions': None,
            'message': str(exception),
            'final': True
        }
    
        response = json.dumps(response).encode()

        self.response_channel.basic_publish(
            exchange='',
            routing_key=os.environ['RESPONSE_QUEUE'],
            body=response,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

    def run(self):

        config_file = os.path.join(
            os.path.realpath(os.environ['DOCKER_TEMP_FOLDER']),
            os.environ['OPTIMIZATION_ID'],
            os.environ['MODEL_FILE_NAME']
        )

        with open(config_file) as f:
            content = json.load(f)

        kwargs = {
            'optimization_id': os.environ['OPTIMIZATION_ID'],
            'request_data': content,
            'response_channel': self.response_channel,
            'response_queue': os.environ['RESPONSE_QUEUE'],
            'rabbit_host': os.environ['RABBITMQ_HOST'], 
            'rabbit_port': os.environ['RABBITMQ_PORT'],
            'rabbit_vhost': os.environ['RABBITMQ_VIRTUAL_HOST'],
            'rabbit_user': os.environ['RABBITMQ_USER'],
            'rabbit_password': os.environ['RABBITMQ_PASSWORD'],
            'simulation_request_queue': os.environ['SIMULATION_REQUEST_QUEUE'],
            'simulation_response_queue': os.environ['SIMULATION_RESPONSE_QUEUE']
        }

        try:
            if content['optimization']['parameters']['method'] == 'GA':
                algorithm = NSGA(
                    **kwargs
                )
            elif content['optimization']['parameters']['method'] == 'Simplex':
                algorithm = NelderMead(
                    **kwargs
                )
        except Exception as e:
            self.reply_error(e)
            self.connection.close()
            raise

        try:
            algorithm.run()
            
        except Exception as e:
            self.reply_error(e)
        
        finally:
            algorithm.clean()
            self.connection.close()


if __name__ == "__main__":
    om = OptimizationManager()
    om.run()


