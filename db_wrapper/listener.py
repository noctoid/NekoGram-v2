#!/usr/bin/python3
import pika
import json

from mongo_connector import MongoDB_Connector

Q_SERVER = "192.168.0.31"
Q_USERNAME = "nekogram"
Q_PASSWORD = "qwer1234"

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=Q_SERVER,
        credentials=pika.PlainCredentials(Q_USERNAME, Q_PASSWORD)
    )
)
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, props, body):
    query = json.loads(body.decode())

    print(" [.] ", query)

    db = MongoDB_Connector()
    response = db.mockup()

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(114514)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
