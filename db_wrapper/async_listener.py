#!/usr/bin/python3
import json
import asyncio
from functools import partial
from aio_pika import connect, IncomingMessage, Exchange, Message
from retriever import Retriever
# this is the part that the program decode database access requests from
# RabbitMQ RPC calls and translate them into actual db requests

# Listens on the RabbitMQ for requests
async def on_message(exchange: Exchange, message: IncomingMessage):
    with message.process():
        # print(message.correlation_id)
        n = message.body.decode()


        # try to parse the request, if fails send status 400 bad request
        print(" [.] ", n, type(n))
        try:
            req = json.loads(n)
            api_version_used = req['ver']
            object_requested = req['object']
            query            = req['query']

            assert api_version_used == "0.1"
            assert object_requested in ["postings", "comments", "likes"]
            assert len(query) > 0

            c = Retriever()
            response = await c.get_posting_by_id(query)
            response["_id"] = "ObjID"
            print(response, type(response))
            response = json.dumps(response)

        except (KeyError, AssertionError):
            print("[!] Invalid Incoming Request ", n)
            response = json.dumps({"status": 400})

        except:
            print("[!] Internal Error ", n)
            response = json.dumps({"status": 500})

        
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