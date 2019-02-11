#!/usr/bin/python3.7

import sys
import asyncio
from aio_pika import connect, Message, DeliveryMode, ExchangeType

class Emitter:
    def __init__(self):
        pass

    async def _connect(self, loop):
        connection = await connect(
            "amqp://guest:guest@localhost/", loop=loop
        )

        # Creating a channel
        channel = await connection.channel()

        logs_exchange = await channel.declare_exchange(
            'logs', ExchangeType.FANOUT
        )
        self.logs_exchange = logs_exchange

    async def emit(self, n):
        msg_body = n.encode()

        message = Message(
            msg_body,
            delivery_mode=DeliveryMode.PERSISTENT
        )
        await self.logs_exchange.publish(message, routing_key='info')

        print("[.] Sent %r" % message)

# testing purpose, to be removed
async def foobar(emitter):
    print("do stuff")
    await emitter.emit("do stuff!")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    emitter = Emitter()
    loop.run_until_complete(emitter._connect(loop))
    loop.run_until_complete(foobar(emitter))

