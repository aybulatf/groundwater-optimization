import pika
import json

with open('./test_optimization_ga.json') as f:
    data = json.load(f)


connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='sheep.rmq.cloudamqp.com',
        port=5672,
        credentials=pika.PlainCredentials('ylfqreqi', 'oe3Hqc_nPWomlp2eDnq5Chwtnfy3jnBk'),
        virtual_host='ylfqreqi'
    )
)

channel = connection.channel()

channel.queue_declare(queue='optimization_request_queue', durable=True)

channel.basic_publish(
    exchange='',
    routing_key='optimization_request_queue',
    body=json.dumps(data).encode()
)

print(" [x] Sent Test Data")
connection.close()