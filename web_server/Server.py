#!/usr/bin/python3

from sanic import Sanic
from sanic.response import json

import json as j

import asyncio

# from connector_base import AsyncPersistenceConnector
from Request_Handler import RequestHandler

app = Sanic()


@app.route("/")
async def test(request):
    return json({"Neko": "Gram!"})


@app.route("/p/read/")
async def p_read(request):
    logic = RequestHandler()
    result = await logic.get_postings()

    return json(j.loads(result))

@app.route("/p/create/")
async def p_create(request):
    logic = RequestHandler()
    result = await logic.create_postings()
    return json(j.loads(result))

@app.route("/p/update")
async def p_update(request):
    return json({"body": "sooooooooon"}, status=501)

@app.route("/p/delete/")
async def p_delete(request):
    return json({"body": "sooooooooon"}, status=501)

@app.route("/c/create/")
async def c_create(request):
    return json({"body": "sooooooooon"}, status=501)

@app.route("/c/read/")
async def c_read(request):
    return json({"body": "sooooooooon"}, status=501)

@app.route("/c/update/"):
async def c_update(request):
    return json({"body": "sooooooooon"}, status=501)

@app.route("/c/delete")
async def c_delete(request):
    return json({"body": "sooooooooon"}, status=501)

@app.route("/l/do/")
async def l_do(request):
    return json({"body": "sooooooooon"}, status=501)

@app.route("/l/undo")
async def l_undo(request):
    return json({"body": "sooooooooon"}, status=501)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
