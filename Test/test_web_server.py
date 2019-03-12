import requests
import json
import pprint
from uuid import uuid4

def post(url, headers, data):
    r = requests.post(url, headers=headers, data=json.dumps(data))
    return r.text


if __name__ == "__main__":
    server = "http://127.0.0.1:8000/"

    user = post(
        "http://127.0.0.1:8000/u/create/",
        {
            "Content-Type": "application/json",
        },
        {
            "username": "testuser1",
            "password": "qwer1234",
            "displayName": "Test"
        }
    )

    token = json.loads(post(
            "http://127.0.0.1:8000/auth/",
            {"Content-Type": "application/json"},
            {"username":"testuser1", "password":"qwer1234"}
    ))
    print(token)
    token = token["access_token"]

    r = json.loads(requests.get("http://127.0.0.1:8000/", headers={"Authorization": "Bearer "+token}).text)

    assert r == {"Neko": "Gram!"}

    headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        }




    print("\n\nTest Read User\n")

    result = json.loads(post(
        "http://127.0.0.1:8000/u/read/",
        headers,
        {
            "username": "testuser1"
        }
    ))
    user = result['result']
    print(user)





    print("\n\nTest Create P\n")
    pid = "00000000-1111-2222-3333-000000000000"

    result = post(
        "http://127.0.0.1:8000/p/create/",
        headers,
        {"pid":pid, "uid": user["uid"], "type":"posting", "content": {
          "txt": "I had In n Out for lunch today and it is good.",
          "hasMedia": True,
          "mimeType": "image/png",
          "mediaUrl": "https://cdn.example.com/img/a-nice-burger.png",

        },
        "comments":[], "likes":[], "repost":[], "public": True}
    )




    print("\n\nTest Update User\n")
    result = post(
        "http://127.0.0.1:8000/u/update/",
        headers,
        {
            "uid": user["uid"],
            "modification": {
                "displayName": "TestModified"
            }
        }
    )




    print("\n\nTest Update P\n")
    result = post(
        "http://127.0.0.1:8000/p/update/",
        headers,
        {
            "pid": pid,
            "modification": {
                "txt": "No more In n Out!"
            }
        }
    )
    pprint.pprint(json.loads(post(
        "http://127.0.0.1:8000/p/read/",
        headers,
        {
            "pid": pid
        }
    )))



    print("\n\nTest Delete User\n")
    result = post(
        "http://127.0.0.1:8000/p/delete/",
        headers,
        {"pid": pid}
    )


    # delete temporary user
    print("\n\nTest Delete User\n")

    result = post(
        "http://127.0.0.1:8000/u/delete/",
        {
            "Content-Type": "application/json",
            "Authorization": "Bearer "+token,
        },
        {"uid": user["uid"]}
    )
    print(result)