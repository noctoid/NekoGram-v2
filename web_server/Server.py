#!/usr/bin/python3

from sanic import Sanic
from sanic_cors import CORS, cross_origin
from sanic.response import json

from sanic_jwt import exceptions
from sanic_jwt import initialize
from sanic_jwt.decorators import protected
from sanic_jwt import Authentication

from jwt import decode as jwt_decode

import json as j

import asyncio

# from connector_base import AsyncPersistenceConnector
from Request_Handler import RequestHandler
from Models import Posting, User

DEV = True

logic = RequestHandler()

# class User:
#
#     def __init__(self, id, username, password):
#         self.user_id = id
#         self.username = username
#         self.password = password
#
#     def __repr__(self):
#         return "User(id='{}')".format(self.user_id)
#
#     def to_dict(self):
#         return {"user_id": self.user_id, "username": self.username}
#
#
# users = [User(1, "noctoid", "qwer1234"), User(2, "user2", "abcxyz")]
#
# username_table = {u.username: u for u in users}
# userid_table = {u.user_id: u for u in users}
#
#
# class MyAuthentication(Authentication):
#
#     async def extend_payload(self, payload, *args, **kwargs):
#         payload.update({"app_name": self.app.name})
#         return payload
#
#     async def authenticate(self, request, *args, **kwargs):
#         username = request.json.get("username", None)
#         password = request.json.get("password", None)
#
#         if not username or not password:
#             raise exceptions.AuthenticationFailed(
#                 "Missing username or password."
#             )
#
#         user = username_table.get(username, None)
#         if user is None:
#             raise exceptions.AuthenticationFailed("User not found.")
#
#         if password != user.password:
#             raise exceptions.AuthenticationFailed("Password is incorrect.")
#
#         return user

async def authenticate(request, *args, **kwargs):
    # print(request.json)
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    result = await logic.auth_user(username, password)
    result = j.loads(result)['result']

    if result['status'] == "failed":
        raise exceptions.AuthenticationFailed("User not found.")
    elif result['status'] == "success":
        if result['auth'] == True:
            user = User(user_id=username, username=username, password=password)
            return user
        else:
            raise exceptions.AuthenticationFailed("Password is incorrect")


app = Sanic()
initialize(app, authenticate=authenticate, secret="secret")
CORS(app)


@app.route("/")
@protected()
async def test(request):
    print(jwt_decode(request.headers['authorization'][7:], "secret"))
    return json({"Neko": "Gram!"})


@app.route("/user", methods=['GET','POST', 'OPTIONS'])
@protected()
async def user_cred(request):
    print("!!!")
    print(jwt_decode(request.headers['authorization'][7:], "secret"))
    return json({
        "userid": jwt_decode(request.headers['authorization'][7:], "secret"),
        "username": "noctoid"
    })




@app.route("/p/read/", methods=['POST', 'OPTIONS'])
@protected()
async def p_read(request):
    # form = request.form
    print(request.json)

    query = request.json
    try:
        pid = str(query['pid'])
        result = await logic.get_postings(pid)
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)

    print(result)
    return json(j.loads(result))

@app.route("/p/read_many/", methods=['POST', 'OPTIONS'])
@protected()
async def p_read_many(request):
    if DEV:
        print(request.json)
    query = request.json
    try:
        result = await logic.get_postings_batch(
            query['list_of_pid']
        )
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)

    if DEV:
        print(result)
    return json(j.loads(result))

@app.route("/p/create/", methods=['POST', 'OPTIONS'])
@protected()
async def p_create(request):
    # logic = RequestHandler()
    print(request.json)
    # try:
    query = request.json

    if DEV:
        result = await logic.create_postings(
            Posting(
                pid=str(query["pid"]),
                uid=str(query['uid']),
                type=str(query["type"]),
                content=query['content'],
                public=bool(query["public"])
            )
        )
    else:
        result = await logic.create_postings(
            Posting(
                uid=str(query['uid']),
                type=str(query["type"]),
                content=query['content'],
                public=bool(query["public"])
            )
        )
    # except (ValueError, IndexError, KeyError):
    #     return json({"status": "bad request"}, status=400)
    return json(j.loads(result))

@app.route("/p/update/", methods=['OPTIONS', 'POST'])
async def p_update(request):
    print(request.json)
    try:
        query = request.json

        result = await logic.update_postings(
            str(query["pid"]),
            query['modification']
        )
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)
    return json(j.loads(result))

@app.route("/p/delete/", methods=['OPTIONS', 'POST'])
async def p_delete(request):
    try:
        query = request.json
        if DEV:
            print(query)
        result = await logic.delete_postings(str(query["pid"]))
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)
    return json(j.loads(result))

@app.route("/p/search/", methods=['OPTIONS', 'POST'])
async def p_search(request):
    return json({"body": "soooooooooon"}, status=200)

@app.route("/p/u_get_plist", methods=['OPTIONS', 'POST'])
@protected()
async def p_user_plist(request):
    if DEV:
        print(request.json)

    try:
        query = request.json
        result = await logic.list_user_postings(
            query['username']
        )
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)
    return json(j.loads(result))


@app.route("/u/create/", methods=['OPTIONS', 'POST'])
async def u_create(request):
    print(request.json)
    try:
        query = request.json

        result = await logic.create_user(
            User(
                username=str(query['username']),
                password=str(query['password']),
                displayName=str(query['displayName'])
            )
        )
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)
    return json(j.loads(result))

@app.route("/u/read/", methods=['OPTIONS', 'POST'])
@protected()
async def u_read_info(request):
    try:
        query = request.json
        # print(query)
        result = await logic.get_user(
            query['username']
        )
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)
    return json(j.loads(result))

@app.route("/u/update/", methods=['OPTIONS', 'POST'])
async def u_update(request):
    print(request.json)
    try:
        query = request.json

        result = await logic.update_user(
            str(query["uid"]),
            query['modification']
        )
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)
    return json(j.loads(result))

@app.route("/u/delete/", methods=["OPTIONS", "POST"])
@protected()
async def u_delete(request):
    try:
        query = request.json
        if DEV:
            print(query)
        result = await logic.delete_user(str(query["uid"]))
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)
    return json(j.loads(result))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
