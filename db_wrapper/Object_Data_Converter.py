#!/usr/bin/python3
import asyncio
from concurrent.futures import ProcessPoolExecutor
from uuid import uuid4


# from mongodb_connector import Async_Mongo_Connector
from s3_connector import new_media, remove_media

class OD_Converter:
    # def __init__(self, db, obj_requested=None, method=None, query=None):
    def __init__(self, db_connection):
        try:
            self.mongo_client = db_connection
        except:
            raise ConnectionError

    async def u_auth(self, username, password):
        user = await self.u_get(username)
        print(user)
        if not user:
            return {"status": "failed", "message": "No such user"}
        return {"status": "success", "auth": user['password'] == password}


    async def p_get(self, list_of_pid):
        result = []
        for q in list_of_pid:
            elem = await self.mongo_client.findByKeyValue(
                "user_content", "postings",
                "pid", q
            )
            elem.pop("_id")
            result.append(elem)
        print("DB->", result)
        return result

    async def p_new(self, P):
        result = await self.mongo_client.InsertByKeyValue(
            "user_content", "postings", P
        )
        print(P["pid"])
        return {"status": 200, "pid": P["pid"]}

    async def p_update(self, pid, modification):
        result = await self.mongo_client.updateByKeyValue(
            "user_content", "postings", "pid", pid, modification
        )
        return {"status": 200}

    async def p_remove(self, list_of_pid):
        for pid in list_of_pid:
            result = await self.mongo_client.deleteByKeyValue(
                "user_content", "postings", "pid", pid
            )
        return {"status": 200}

    async def u_new(self, new_user):
        isUserExist = await self.mongo_client.findByKeyValue(
            "user_content", "profiles", "username", new_user["username"]
        )
        if isUserExist:
            return {"status": 403, "message": "username taken"}
        result = await self.mongo_client.InsertByKeyValue(
            "user_content", "profiles", new_user
        )
        return {"status": 200}

    async def u_get(self, username):
        result = await self.mongo_client.findByKeyValue(
            "user_content", "profiles", "username", username
        )
        return result

    async def u_get_by_id(self, uid):
        result = await self.mongo_client.findByKeyValue(
            "user_content", "profiles", "uid", uid
        )
        print(result)
        return result

    async def u_get_plist(self, username):
        user = await self.u_get(username)
        return user['postings']

    async def u_remove(self, list_of_uid):
        for uid in list_of_uid:
            result = await self.mongo_client.deleteByKeyValue(
                "user_content", "profiles", "uid", uid
            )
        return {"status": 200}

    async def u_update(self, uid, modification):
        result = await self.mongo_client.updateByKeyValue(
            "user_content", "profiles", "uid", uid, modification
        )
        return {"status": 200, "message": "user updated"}

    async def u_update_postings(self, uid, modification):
        result = await self.mongo_client.insertToListByKeyValue(
            "user_content", "profiles", "uid", uid, modification
        )
        return {"status": 200, "message": "user postings updated"}

    async def m_new(self, s3, media):
        media_id = str(uuid4())
        result = await new_media(s3, media_id, media)
        if result:
            return {"media_url": result}
        else:
            return {"status": "403", "message": "not a valid media file"}

    async def m_remove(self, s3, media_key):
        result = await remove_media(s3, media_key)
        return {"status": "200", "message": "done"}



if __name__ == "__main__":
    c = OD_Converter()
    loop = asyncio.get_event_loop()
    c.load("postings", "read", {
        "payload": {
            "posting-id": 1234567
        }
    })
    result = loop.run_until_complete(c.p_read())

    print(result)
