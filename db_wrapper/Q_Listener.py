#!/usr/bin/python3
import json
import asyncio
from functools import partial
from aio_pika import connect, IncomingMessage, Exchange, Message
from Object_Data_Converter import OD_Converter
from pprint import pprint
from NekoLogger.Emitter import Emitter
from MongoDB_Connector import Async_Mongo_Connector

logger = Emitter()

db = Async_Mongo_Connector(ip="10.0.1.235")
# this is the part that the program decode database access requests from
# RabbitMQ RPC calls and translate them into actual db requests

# Listens on the RabbitMQ for requests
async def on_message(exchange: Exchange, message: IncomingMessage):
    with message.process():
        # print(message.correlation_id)
        n = message.body.decode()


        # try to parse the request, if fails send status 400 bad request
        try:
            req = json.loads(n)
            api_version_used = req['ver']
            method_used      = req["method"]
            object_requested = req['object']
            query            = req['query']

            assert api_version_used == "0.1"
            assert method_used in ['read', 'delete', 'update', 'create', "batch_read", "user_plist", "checkpwd"]
            assert object_requested in ["postings", "comments", "likes", "profiles"]
            assert len(query) > 0

            # parse query fetched from Q
            # get data as desired object
            odc = OD_Converter(
                db,
                obj_requested=object_requested,
                method=method_used,
                query=query
            )
            db_response = await odc.do()
            response = {}
            print(response)

            if db_response != None:
                if "_id" in db_response:
                    db_response.pop("_id")
                n = "[.] done " + n
                response["status"] = "done"
                response["result"] = db_response
                response = json.dumps(response)
            # print(response, type(response))
            if response is None:
                n = "[!] Not Found "+n
                response = json.dumps({"status": "not found"})

        except (KeyError, AssertionError):
            response = json.dumps({"status": 400, "message": n})
            n = "[!] Invalid Incoming Request "+ n

        except ConnectionError:
            response = json.dumps({"status": 500, "message": n})
            n = "[!] Failed to Connect Database " + n

        # except:
        #     response = json.dumps({"status": 500, "message": n})
        #     n = "[!] Internal Error " + n

        # return the object requested found in db back to the RPC
        await exchange.publish(
            Message(
                body=response.encode(),
                correlation_id=message.correlation_id
            ),
            routing_key=message.reply_to
        )
        # log
        print(n)
        await logger.emit(n, tee=False)


async def main(loop):
    # Perform connection
    # connection = await connect(
    #     host="192.168.0.32",
    #     login="nekogram",
    #     password="qwer1234",
    # )
    await logger.connect(loop)
    connection = await connect("amqp://guest:guest@127.0.0.1/", loop=loop)

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
    print("[i] Awaiting RPC requests")
    loop.run_forever()