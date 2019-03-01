#!/usr/bin/python3

from sanic import Sanic
from sanic_cors import CORS, cross_origin
from sanic.response import json

import json as j

import asyncio

# from connector_base import AsyncPersistenceConnector
from Request_Handler import RequestHandler

app = Sanic()
CORS(app)
logic = RequestHandler()


@app.route("/")
async def test(request):
    return json({"Neko": "Gram!"})


@app.route("/p/read/", methods=['POST', 'OPTIONS'])
async def p_read(request):
    # form = request.form
    print(request)
    # try:
    #     result = await logic.get_postings(
    #         str(form['key'][0]),
    #         str(form['value'][0]))
    # except (ValueError, IndexError, KeyError):
    #     return json({"status": "bad request"}, status=400)

    form = request.json
    try:
        result = await logic.get_postings(
            str(form['key']),
            str(form['value']))
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)

    print(result)
    return json(j.loads(result))

@app.route("/p/create/", methods=['POST'])
async def p_create(request):
    # logic = RequestHandler()
    try:
        form = request.form
        result = await logic.create_postings(
            str(form["uid"][0]),
            str(form["txt"][0]),
            str(form["mime"][0]),
            str(form["media_url"][0])
        )
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)
    return json(j.loads(result))

@app.route("/p/update")
async def p_update(request):
    return json({"body": "sooooooooon"}, status=501)

@app.route("/p/delete/")
async def p_delete(request):
    return json({"body": "sooooooooon"}, status=501)

@app.route("/p/search/", methods=['OPTIONS', 'POST'])
async def p_search(request):
    return json({"body": "soooooooooon"}, status=200)

@app.route("/c/create/")
async def c_create(request):
    return json({"body": "sooooooooon"}, status=501)

@app.route("/c/read/")
async def c_read(request):
    return json({"body": "sooooooooon"}, status=501)

@app.route("/c/update/")
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

@app.route("/u/create/", methods=['OPTIONS', 'POST'])
async def u_create(request):
    return json({"body": "sooon"}, status=200)

@app.route("/u/read_info/", methods=['OPTIONS', 'POST'])
async def u_read_info(request):
    return json({"body": "soon"}, status=200)

@app.route("/u/update/", methods=['OPTIONS', 'POST'])
async def u_update(request):
    return json({"body": "sooon"}, status=200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
