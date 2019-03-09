import requests
import json
import pprint

def post(url, headers, data):
    r = requests.post(url, headers=headers, data=json.dumps(data))
    return r.text


if __name__ == "__main__":
    server = "http://127.0.0.1:8000/"

    token = json.loads(post(
            "http://127.0.0.1:8000/auth/",
            {"Content-Type": "application/json"},
            {"username":"noctoid", "password":"qwer1234"}
    ))
    print(token)
    token = token["access_token"]

    r = json.loads(requests.get("http://127.0.0.1:8000/", headers={"Authorization": "Bearer "+token}).text)

    assert r == {"Neko": "Gram!"}

    tests = [
        # {
        #     "url":"http://127.0.0.1:8000/p/read/",
        #     "headers": {
        #         "Content-Type": "application/json",
        #         "Authorization": "Bearer "+token,
        #     },
        #     "data": {
        #         "key": "pid",
        #         "value": "31a47ed1-2752-4482-9049-5257a6ec0962"
        #     }
        # },
        # {
        #     "url":"http://127.0.0.1:8000/p/read/",
        #     "headers": {
        #         "Content-Type": "application/json",
        #         "Authorization": "Bearer "+token,
        #     },
        #     "data": {
        #         "key": "pid",
        #         "value": "2128cbf7-2284-48a6-8fac-69e9b4bccc95"
        #     }
        # },
        # {
        #     "url": "http://127.0.0.1:8000/u/create/",
        #     "headers": {
        #         "Content-Type": "application/json"
        #     },
        #     "data": {
        #         "username": "noctoid",
        #         "password": "qwer1234",
        #         "displayName": "Noctoid"
        #     }
        # },
        # {
        #     "url": "http://127.0.0.1:8000/u/read/",
        #     "headers": {
        #         "Content-Type": "application/json",
        #         "Authorization": "Bearer " + token,
        #     },
        #     'data': {
        #         "username": "noctoid"
        #     }
        # },
        # {
        #     "url": "http://127.0.0.1:8000/p/read_many/",
        #     "headers": {
        #         "Content-Type": "application/json",
        #         "Authorization": "Bearer " + token,
        #     },
        #     'data': {
        #         "list_of_pid": [
        #             "2128cbf7-2284-48a6-8fac-69e9b4bccc95",
        #             "31a47ed1-2752-4482-9049-5257a6ec0962",
        #         ]
        #     }
        # },
        {
            "url": "http://127.0.0.1:8000/p/user_plist/",
            "headers" : {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            },
            'data': {
                "uid": "e8be2184-642e-4517-84ad-8cbec50b05c8"
            }
        }
    ]

    answers = [
        # {'result': {'_id': 'ObjID',
        #             'comments': '0a67d109-a46b-4aef-a4b2-9b729d938802',
        #             'likes': '1f0e8396-aaab-4a01-8a57-64489adc91ae',
        #             'media_url': 'https://cdn.vox-cdn.com/thumbor/-bKrYahnwqww9sH9v2h34v9ViA0=/0x114:585x559/1200x800/filters:focal(248x297:340x389)/cdn.vox-cdn.com/uploads/chorus_image/image/57272301/Screen_Shot_2017_10_23_at_10.16.32_AM.0.png',
        #             'mime': 'image/png',
        #             'pid': '31a47ed1-2752-4482-9049-5257a6ec0962',
        #             'uid': '1234567',
        #             'valid': True},
        #  'status': 'done'},
        # {'result': {'_id': 'ObjID',
        #             'comments': '23741d10-1098-49d0-8f48-b0304a5a4b25',
        #             'likes': '69fceafa-3f22-4f75-8339-a988ac802248',
        #             'media_url': 'https://cdn.vox-cdn.com/thumbor/-bKrYahnwqww9sH9v2h34v9ViA0=/0x114:585x559/1200x800/filters:focal(248x297:340x389)/cdn.vox-cdn.com/uploads/chorus_image/image/57272301/Screen_Shot_2017_10_23_at_10.16.32_AM.0.png',
        #             'mime': 'image/png',
        #             'pid': '2128cbf7-2284-48a6-8fac-69e9b4bccc95',
        #             'uid': '1234567',
        #             'valid': True},
        #  'status': 'done'},
        # {'result': {'status': 200}, 'status': 'done'},
        # {},
        # {},
        {}

    ]


    for t,a in zip(tests, answers):
        pprint.pprint(json.loads(post(t["url"], t['headers'], t['data'])))
        # assert json.loads(post(t["url"], t['headers'], t['data'])) == a