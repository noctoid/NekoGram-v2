#!/usr/bin/python3
# import pika
import uuid
import json

import asyncio
from aio_pika import connect, connect_robust, IncomingMessage, Message

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


# class PersistenceConnector(object):
#     def __init__(self):
#         self.connection = pika.BlockingConnection(
#             pika.ConnectionParameters(
#                 host=Q_SERVER,
#                 credentials=pika.PlainCredentials(Q_USERNAME, Q_PASSWORD)
#             )
#         )

#         self.channel = self.connection.channel()

#         result = self.channel.queue_declare(exclusive=True)
#         self.callback_queue = result.method.queue

#         self.channel.basic_consume(
#             self.on_response, no_ack=True, queue=self.callback_queue
#         )

#     def on_response(self, ch, method, props, body):
#         if self.corr_id == props.correlation_id:
#             self.response = body

#     def call(self, obj):
#         self.response = None
#         self.corr_id = str(uuid.uuid4())
#         self.channel.basic_publish(
#             exchange='',
#             routing_key='rpc_queue',
#             properties=pika.BasicProperties(
#                  reply_to=self.callback_queue,
#                  correlation_id=self.corr_id,
#             ),
#             body=json.dumps(obj)
#         )
#         while self.response is None:
#             self.connection.process_data_events()
#         return self.response


class AsyncPersistenceConnector:
    def __init__(self, loop):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}
        self.loop = loop

    async def connect(self):
        # self.connection = await connect_robust(
        #     host="127.0.0.1",
        #     login="nekogram",
        #     password="qwer1234",
        #     loop=loop
        # )
        self.connection = await connect("amqp://guest:guest@127.0.0.1/", loop=loop)
        self.channel = await self.connection.channel(publisher_confirms=False)
        self.callback_queue = await self.channel.declare_queue(
            exclusive=True
        )
        await self.callback_queue.consume(self.on_response)

        return self

    def on_response(self, message: IncomingMessage):
        future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)

    async def call(self, n):
        correlation_id = str(uuid.uuid4()).encode()
        print(correlation_id)
        future = self.loop.create_future()

        self.futures[correlation_id] = future
        await self.channel.default_exchange.publish(
            Message(
                "shit".encode(),
                content_type="text/plain",
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
            ),
            routing_key='rpc_queue',
        )

        return await future


async def main(loop):
    a_db_rpc = await AsyncPersistenceConnector(loop).connect()
    print(" [x] Requesting sample query async")
    response = await a_db_rpc.call(sample_query)
    print(" [.] Got %r" % response)


if __name__ == "__main__":
    # db_rpc = PersistenceConnector()
    # print(" [x] Requesting sample query")
    # response = db_rpc.call(sample_query)
    # print(" [.] Got", response)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
