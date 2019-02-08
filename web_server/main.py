#!/usr/bin/python3

from sanic import Sanic
from sanic.response import json

import json as j

import asyncio

# from connector_base import AsyncPersistenceConnector
from logic import Logic

app = Sanic()


@app.route("/")
async def test(request):
    return json({"Neko": "Gram!"})


@app.route("/p/read/")
async def post_read(request):
    logic = Logic()
    result = await logic.get_postings()

    return json(j.loads(result))

@app.route("/p/create/")
async def post_create(request):
    logic = Logic()
    result = await logic.create_postings()
    return json(j.loads(result))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
