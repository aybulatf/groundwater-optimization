import os
import sys
import pika
import warnings
import json

from Optimization import NSGA, NelderMead


DATA_FOLDER = os.environ['DATA_FOLDER']
HOST = os.environ['HOST']
PORT = os.environ['PORT']
VIRTUAL_HOST = os.environ['VIRTUAL_HOST']
USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
REQUEST_QUEUE = os.environ['REQUEST_QUEUE']
RESPONSE_QUEUE = os.environ['RESPONSE_QUEUE']
SIMULATION_REQUEST_QUEUE = os.environ['SIMULATION_REQUEST_QUEUE']
SIMULATION_RESPONSE_QUEUE = os.environ['SIMULATION_RESPONSE_QUEUE']

warnings.filterwarnings("ignore")
CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=HOST,
        port=int(PORT),
        virtual_host=VIRTUAL_HOST,
        credentials=pika.PlainCredentials(USER, PASSWORD),
        heartbeat_interval=0
    )
)

def on_request(ch, method, props, body):

    content = json.loads(body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print('Summary of the optimization problem:')
    print('Author: %s' % content.get("author"))
    print('Project: %s' % content.get("project"))
    print('Model Id: %s' % content.get("model_id"))
    print('Type: %s' % content.get("type"))
    print('Version: %s' % content.get("version"))

    response_channel = CONNECTION.channel()
    response_channel.queue_declare(queue=RESPONSE_QUEUE, durable=True)

    kwargs = {
        'request_data': content,
        'response_channel': response_channel,
        'response_queue': RESPONSE_QUEUE,
        'data_folder': DATA_FOLDER,
        'rabbit_host': HOST, 
        'rabbit_port': PORT,
        'rabbit_vhost': VIRTUAL_HOST,
        'rabbit_user': USER,
        'rabbit_password': PASSWORD,
        'simulation_request_queue': SIMULATION_REQUEST_QUEUE,
        'simulation_response_queue': SIMULATION_RESPONSE_QUEUE
    }

    try:
        if content['optimization']['parameters']['method'] == 'GA':
            optimization = NSGA(
                **kwargs
            )
        elif content['optimization']['parameters']['method'] == 'Simplex':
            optimization = NelderMead(
                **kwargs
            )
        optimization.run()
        optimization.clean()
        

    except Exception as e:
        response = {
            'status_code': "500",
            'solutions': None,
            'message': str(e),
            'final': True
        }
        
        response = json.dumps(response).encode()

        response_channel.basic_publish(
            exchange='',
            routing_key=RESPONSE_QUEUE,
            body=response,
            properties=pika.BasicProperties(
                delivery_mode=2  # make message persistent
            )
        )


if __name__ == "__main__":

    read_channel = CONNECTION.channel()
    read_channel.queue_declare(queue=REQUEST_QUEUE, durable=True)

    read_channel.basic_qos(prefetch_count=1)
    read_channel.basic_consume(on_request, queue=REQUEST_QUEUE)

    print(" [x] Optimization server awaiting requests")
    read_channel.start_consuming()


