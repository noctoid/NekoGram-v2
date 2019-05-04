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
            if elem:
                elem.pop("_id")
                result.append(elem)
            else:
                result.append({"uid":"0", "pid": q, "content": {"txt": "Posting Unavailable"}})
        print("!!!",result)
        # list_of_uid = [posting["uid"] for posting in result]
        list_of_uid = []
        for posting in result:
            if posting["uid"] != "0":
                list_of_uid.append(posting["uid"])
        print("!!!", list_of_uid)
        authors = await self.p_get_author_info(list_of_uid)
        for r in result:
            if r['uid'] == "0":
                pass
            else:
                r["username"] = authors[r["uid"]]["username"]
                r["displayName"] = authors[r["uid"]]["displayName"]
                r["avatarUrl"] = authors[r["uid"]]["avatarUrl"]
        print("DB->", result)
        return result

    async def p_get_author_info(self, list_of_uid):
        result = {}
        for uid in list_of_uid:
            if uid not in result:
                user = await self.u_get_by_id(uid)
                result[uid] = {
                    "username": user["username"],
                    "displayName": user["displayName"],
                    "avatarUrl": user["avatarUrl"]
                }
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

    async def p_update_after_like(self, pid, modification):
        result = await self.mongo_client.insertToListByKeyValue(
            "user_content", "postings", "pid", pid, modification
        )
        return {"status": 200, "message": "user postings updated"}

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

    async def u_update_postings_after_delete(self, uid, modification):
        result = await self.mongo_client.pullToListByKeyValue(
            "user_content", "profiles", "uid", uid, modification
        )
        print(result)
        return {"status": 200, "message": "user postings updated"}

    async def search(self, query):
        results = \
            await self.mongo_client.findByKeyValueApprox("user_content", "profiles", "username", query)+ \
            await self.mongo_client.findByKeyValueApprox("user_content", "profiles", "displayName", query)+ \
            await self.mongo_client.findByKeyValueApprox("user_content", "postings", "content.txt", query)
        posting_results = []
        for result in results:
            if not result.get("username", None):
                posting_results.append(result.get("uid", None))
        author_info = await self.p_get_author_info(posting_results)
        for r in results:
            if not r.get("username", None):
                r["username"] = author_info[r["uid"]]["username"]
                r["displayName"] = author_info[r["uid"]]["displayName"]
                r["avatarUrl"] = author_info[r["uid"]]["avatarUrl"]
        return results

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
