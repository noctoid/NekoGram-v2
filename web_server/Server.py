#!/usr/bin/python3

from sanic import Sanic
from sanic_cors import CORS, cross_origin
from sanic.response import json
from sanic_jwt import exceptions
from sanic_jwt import initialize
from sanic_jwt.decorators import protected

import json as j

import asyncio

# from connector_base import AsyncPersistenceConnector
from Request_Handler import RequestHandler
from Models import Posting, User


class User1:

    def __init__(self, id, username, password):
        self.user_id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "User(id='{}')".format(self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}


users = [User1(1, "user1", "abcxyz"), User1(2, "user2", "abcxyz")]

username_table = {u.username: u for u in users}
userid_table = {u.user_id: u for u in users}


async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = username_table.get(username, None)
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if password != user.password:
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user


app = Sanic()
initialize(app, authenticate=authenticate)
CORS(app)
logic = RequestHandler()


@app.route("/")
@protected()
async def test(request):
    return json({"Neko": "Gram!"})




@app.route("/p/read/", methods=['POST', 'OPTIONS'])
@protected()
async def p_read(request):
    # form = request.form
    print(request)

    query = request.json
    try:
        result = await logic.get_postings(
            str(query['key']),
            str(query['value']))
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)

    print(result)
    return json(j.loads(result))

@app.route("/p/create/", methods=['POST', 'OPTIONS'])
@protected()
async def p_create(request):
    # logic = RequestHandler()
    print(request)
    try:
        query = request.json

        result = await logic.create_postings_2(
            Posting(
                uid=str(query['uid']),
                txt=str(query['txt']),
                mime=str(query['mime']),
                media_url=str(query['media_url'])
            )
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
    print(request)
    try:
        query = request.json

        result = await logic.create_user(
            User(
                nickname=str(query['nickname']),
                password=str(query['password'])
            )
        )
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)
    return json(j.loads(result))

@app.route("/u/read_info/", methods=['OPTIONS', 'POST'])
async def u_read_info(request):
    return json({"body": "soon"}, status=200)

@app.route("/u/update/", methods=['OPTIONS', 'POST'])
async def u_update(request):
    return json({"body": "sooon"}, status=200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
