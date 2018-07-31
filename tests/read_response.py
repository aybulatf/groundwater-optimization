import pika
import json
import uuid


connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='sheep.rmq.cloudamqp.com',
        port=5672,
        credentials=pika.PlainCredentials('ylfqreqi', 'oe3Hqc_nPWomlp2eDnq5Chwtnfy3jnBk'),
        virtual_host='ylfqreqi'
    )
)

channel = connection.channel()

channel.queue_declare(queue='optimization_response_queue', durable=True)

results=[]
consumer_tag = str(uuid.uuid4())
def consumer_callback(channel, method, properties, body):
    content = json.loads(body.decode())
    results.append(content)
    if len(results) >= 29:
        channel.basic_cancel(
            consumer_tag=consumer_tag
        )
    return
channel.basic_consume(
    queue='optimization_response_queue',
    consumer_callback=consumer_callback,
    consumer_tag=consumer_tag
)

channel.start_consuming()

with open('./results.json', 'w') as f:
    json.dump(results, f)

connection.close()