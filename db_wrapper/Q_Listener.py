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
            method = req.get('method', None)
            payload = req.get('payload', None)

            assert method in [
                'p.get', 'p.new', 'p.update', 'p.remove',
                'u.get_plist', 'u.get', 'u.auth', 'u.new', 'u.remove', 'u.update', 'u.freeze',
                'm.new', 'm.remove'
            ]
            assert type(payload) == dict

            odc = OD_Converter(db)

            if method == "p.get":
                db_response = await odc.p_get(payload.get('list_of_pid', []))
            elif method == "p.new":
                db_response = await odc.p_new(payload.get('new_post', None))
            elif method == "p.update":
                db_response = await odc.p_update(payload.get("pid", None), payload.get('modification', None))
            elif method == "p.remove":
                db_response = await odc.p_remove(payload.get('list_of_pid', []))

            elif method == "u.auth":
                db_response = await odc.u_auth(payload.get('username', None), payload.get('password', None))
            elif method == "u.get_plist":
                db_response = await odc.u_get_plist(payload.get('username', None))
            elif method == "u.get":
                db_response = await odc.u_get(payload.get("username", None))
            elif method == "u.new":
                db_response = await odc.u_new(payload.get("new_user", None))
            elif method == "u.remove":
                db_response = await odc.u_remove(payload.get("list_of_uid", []))
            elif method == "u.update":
                db_response = await odc.u_update(payload.get("uid", None), payload.get("modification", None))

            elif method == "m.new":
                db_response = await

            response = {}

            if db_response != None:
                if "_id" in db_response:
                    db_response.pop("_id")
                n = "[.] done " + n
                response["status"] = "done"
                response["result"] = db_response
                response = json.dumps(response)
            # print(response, type(response))
            if response is None:
                response = json.dumps({"status": 404, "message": n})
                n = "[!] Not Found " + n

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

        print(response)

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