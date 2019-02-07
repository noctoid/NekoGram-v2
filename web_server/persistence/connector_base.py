#!/usr/bin/python3.7
# import pika
import uuid
import json

import asyncio
from aio_pika import connect, IncomingMessage, Message

# from settings import Q_SERVER, Q_USERNAME, Q_PASSWORD

Q_SERVER = "192.168.0.31"
Q_USERNAME = "nekogram"
Q_PASSWORD = "qwer1234"


sample_query = {
    "ver": "0.1",
    "object": "postings",
    "query" : {
        "method": "read",
        "payload": {
          "posting-id": 1234567,
        }
    }
}


class AsyncPersistenceConnector:
    def __init__(self, loop):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}
        self.loop = loop

    async def connect(self):
        self.connection = await connect(
            host="192.168.0.32",
            login="nekogram",
            password="qwer1234",
        )
        # self.channel = await self.connection.channel(publisher_confirms=False)
        self.channel = await self.connection.channel()
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
                json.dumps(n).encode(),
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
