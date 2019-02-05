#!/usr/bin/python3
import pika
import uuid
import json

# from settings import Q_SERVER, Q_USERNAME, Q_PASSWORD

Q_SERVER = "192.168.0.31"
Q_USERNAME = "nekogram"
Q_PASSWORD = "qwer1234"


sample_query = {
    "db": "user-content",
    "colle": "postings",
    "query": {
        "key": "post-id",
        "value": 1234567
    }
}


class PersistenceConnector(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=Q_SERVER,
                credentials=pika.PlainCredentials(Q_USERNAME, Q_PASSWORD)
            )
        )

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            self.on_response, no_ack=True, queue=self.callback_queue
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, obj):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                 reply_to=self.callback_queue,
                 correlation_id=self.corr_id,
            ),
            body=json.dumps(obj)
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response


if __name__ == "__main__":
    db_rpc = PersistenceConnector()
    print(" [x] Requesting sample query")
    response = db_rpc.call(sample_query)
    print(" [.] Got", response)
