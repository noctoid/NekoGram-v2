#!/usr/bin/python3

from sanic import Sanic
from sanic.response import json

import json as j

import asyncio

from persistence.connector_base import AsyncPersistenceConnector

app = Sanic()


@app.route("/")
async def test(request):
    return json({"Neko": "Gram!"})


@app.route("/p/read/")
async def post_read(request):
    aio_db = await AsyncPersistenceConnector(asyncio.get_event_loop()).connect()
    result = await aio_db.call({
        "ver": "0.1",
        "object": "postings",
        "method": "read",
        "query" : {
            "payload": {
              "posting-id": 1234567,
            }
        }
    })

    return json(j.loads(result))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
