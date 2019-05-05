#!/usr/bin/python3

from sanic import Sanic
from sanic_cors import CORS, cross_origin
from sanic.response import json
from sanic.response import html

from sanic_jwt import exceptions
from sanic_jwt import initialize
from sanic_jwt.decorators import protected
from sanic_jwt import Authentication

from jwt import decode as jwt_decode

from base64 import b64encode

from uuid import uuid4

import json as j

import asyncio

# from connector_base import AsyncPersistenceConnector
from Request_Handler import RequestHandler
from Models import Posting, User

from NekoGram_Media_Uploader.initiator import Initiator

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('web_server', 'templates'))

DEV = True

logic = RequestHandler()

initiator = Initiator()


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
initialize(
    app,
    authenticate=authenticate,
    url_prefix="/api/auth",
    secret="secret"
)
CORS(app)


@app.route("/", methods=['GET', 'POST', 'OPTIONS'])
@protected()
async def test(request):
    # print(jwt_decode(request.headers['authorization'][7:], "secret"))
    print(request.json)
    return json({"Neko": "Gram!"})


@app.route("/api/register", methods=["GET"])
async def register(request):
    template = env.get_template('register.html')
    return html(template.render())


@app.route("/user", methods=['GET', 'POST', 'OPTIONS'])
@protected()
async def user_cred(request):
    print("!!!")
    print(jwt_decode(request.headers['authorization'][7:], "secret"))
    return json({
        "userid": jwt_decode(request.headers['authorization'][7:], "secret"),
        "username": "noctoid"
    })


@app.route("/api/p/read/", methods=['POST', 'OPTIONS'])
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


@app.route("/api/p/read_my_posts/", methods=['POST', 'OPTIONS'])
@protected()
async def p_read_my_posts(request):
    if DEV:
        print(request.json)

    # get user's all postings first
    my_pids = await logic.list_user_postings(
        request.json['username']
    )
    my_pids = j.loads(my_pids)
    if my_pids["status"] == "done":
        my_pids = my_pids['result']
    else:
        return json({"status": "error", "message": "no such user"}, status=404)

    # then get all posting content
    result = await logic.get_postings_batch(my_pids)
    result = j.loads(result)

    # then fill in liked root content
    # 1. get a list of likes and reposts pid
    need_root_content_pids = [r['root'] for r in result['result'] if r['root']]
    print("1->", need_root_content_pids)
    # 2. get content for the list of pids
    root_contents = j.loads(await logic.get_postings_batch(need_root_content_pids))['result']
    print("2->", root_contents)
    # 3. fill in the root content
    root_contents_map_to_pid = {}
    for root_content in root_contents:
        root_contents_map_to_pid[root_content['pid']] = root_content
    for r in result['result']:
        if r['root']:
            r['root_content'] = root_contents_map_to_pid[r['root']]

    # 4. reverse chronological order
    result['result'].reverse()

    if DEV:
        print(result)

    # except (ValueError, IndexError, KeyError):
    #     return json({"status": "bad request"}, status=400)

    return json(result)


@app.route("/api/p/create/", methods=['POST', 'OPTIONS'])
@protected()
async def p_create(request):
    # logic = RequestHandler()
    print(request.json)
    # try:
    query = request.json

    if DEV:
        try:
            result = await logic.create_postings(
                Posting(
                    pid=str(query["pid"]),
                    uid=str(query['uid']),
                    type=str(query["type"]),
                    content=query['content'],
                    public=bool(query["public"])
                )
            )
        except KeyError:
            result = await logic.create_postings(
                Posting(
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
    # return json(j.loads(result))
    return json(result)


@app.route("/api/p/new_media/", methods=["POST", "OPTIONS"])
@protected()
async def new_media(request):
    if DEV:
        print(request.json)
    try:
        data = request.json.get("data", None)
        if data:
            await initiator.connect(asyncio.get_event_loop())
            _, data = data.split(",")
            mediaUrl = str(uuid4())
            await initiator.emit(data, mediaUrl)
            return json({"status": "done", "result": "media/" + mediaUrl})
        else:
            return json({"status": "error", "message": "not valid media file"}, status=400)


    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)


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


@app.route("/api/p/delete/", methods=['OPTIONS', 'POST'])
async def p_delete(request):
    try:
        query = request.json

        if DEV:
            print(query)

        pid = str(query.get("pid", None))
        uid = str(query.get("uid", None))
        result = await logic.delete_postings(uid, pid)
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)
    return json(j.loads(result))


@app.route("/p/search/", methods=['OPTIONS', 'POST'])
async def p_search(request):
    return json({"body": "soooooooooon"}, status=200)


@app.route("/api/p/like/", methods=['OPTIONS', 'POST'])
@protected()
async def like_by_pid(request):
    if DEV:
        print(request.json)
    try:
        pid = request.json.get("pid", None)
        uid = request.json.get("uid", None)
        result = await logic.like(uid, pid)

    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request", "request": request.json}, status=400)
    return json(result)


@app.route("/api/p/u_get_plist/", methods=['GET', 'OPTIONS', 'POST'])
@protected()
async def p_user_plist(request):
    try:
        if DEV:
            print("p_user_plist: ", request.json)
        query = request.json
        result = await logic.list_user_postings(
            query['username']
        )
    except (ValueError, IndexError, KeyError):
        return json({"status": "bad request"}, status=400)
    return json(j.loads(result), status=200)


@app.route("/api/search/", methods=["OPTIONS", "POST"])
@protected()
async def u_search(request):
    if DEV: print(request.json)

    try:
        query = request.json.get("query", None)
        assert query != None

        response = {"query": query, "result": await logic.search(query)}
    except (AssertionError):
        return json({"status": "bad request", "request": request.json}, status=400)
    return json(response)


@app.route('/api/u/follow/', methods=["OPTIONS", "POST"])
@protected()
async def u_follow(request):
    return json({"follow": "user"})


@app.route("/api/u/create/", methods=["GET", 'OPTIONS', 'POST'])
async def u_create(request):
    # print(request.json)
    print(request.form)
    try:
        query = request.form

        username = str(query['username'][0])
        password = str(query['password'][0])
        displayName = str(query['displayName'][0])

        print(username, password, displayName)

        assert len(username) < 30
        for char in username: assert char in "abcdefghijklmnopqrstuvwxyz0123456789_"
        assert len(password) >= 8
        assert len(password) < 100
        for char in password: assert char in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+-=[]{}\\|;:'\",<.>/?"
        assert len(displayName) < 30
        assert set(displayName) != {" "}

        result = await logic.create_user(
            User(
                username=username,
                password=password,
                displayName=displayName
            )
        )
        print(result)
        result = j.loads(result)

        if result["status"] == "done" and result["result"]["status"] == 200:
            template = env.get_template("done.html")
            return html(template.render())
        elif result["status"] == "done" and result["result"]["status"] == 403:
            template = env.get_template("error.html")
            return html(template.render(message="Username Taken"), status=400)
        else:
            template = env.get_template("error.html")
            return html(template.render(message="Something Went Wrong"), status=400)

    except (ValueError, IndexError, KeyError, AssertionError):
        template = env.get_template("error.html")
        return html(template.render(message="Something Went Wrong"), status=400)

@app.route("/api/u/read/", methods=['OPTIONS', 'POST'])
@protected()
async def u_read(request):
    # return json([{'id': 1, 'username': 'test', 'password': 'test', 'firstName': 'Test', 'lastName': 'User'}])
    if DEV: print(request.json)
    try:
        username = request.json.get("username", None)
        result = await logic.get_user(username)
        # print("user -> ", result)
    except (ValueError, KeyError, IndexError):
        return json({"status": "bad request"}, status=400)
    return json(j.loads(result), status=200)
    # return json(j.loads(result))


@app.route("/api/u/update/", methods=['OPTIONS', 'POST'])
async def u_update(request):
    print(request.json)
    # try:
    query = request.json
    username = request.json.get("username", None)
    profile = await logic.get_user(username)
    profile = j.loads(profile)["result"]
    for key in request.json:
        if request.json[key]:
            profile[key] = request.json[key]
    result = await logic.update_user(
        str(profile["uid"]),
        profile
    )
    # except (ValueError, IndexError, KeyError):
    #     return json({"status": "bad request"}, status=400)
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
