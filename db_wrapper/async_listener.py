#!/usr/bin/python3
import json
import asyncio
from functools import partial
from aio_pika import connect, IncomingMessage, Exchange, Message


async def on_message(exchange: Exchange, message: IncomingMessage):
    with message.process():
        print(message.correlation_id)
        n = message.body.decode()

        print(" [.] ", n, type(n))
        obj = json.loads(n)
        response = obj["db"]
        
        await exchange.publish(
            Message(
                body=response.encode(),
                correlation_id=message.correlation_id
            ),
            routing_key=message.reply_to
        )
        print('Request complete')


async def main(loop):
    # Perform connection
    # connection = await connect_robust(
    #     host="127.0.0.1",
    #     login="nekogram",
    #     password="qwer1234",
    #     loop=loop
    # )
    connection = await connect(
        host="192.168.0.32",
        login="nekogram",
        password="qwer1234",
    )
    # connection = await connect("amqp://guest:guest@127.0.0.1/", loop=loop)

    # Creating a channel
    # channel = await connection.channel(publisher_confirms=False)
    channel = await connection.channel()

    # Declaring queue
    queue = await channel.declare_queue('rpc_queue')

    # Start listening the queue with name 'hello'
    await queue.consume(
        partial(
            on_message,
            channel.default_exchange
        )
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))

    # we enter a never-ending loop that waits for data
    # and runs callbacks whenever necessary.
    print(" [x] Awaiting RPC requests")
    loop.run_forever()