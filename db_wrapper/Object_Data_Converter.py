#!/usr/bin/python3
import asyncio


# from mongodb_connector import Async_Mongo_Connector


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


    # All write methods
    async def p_new(self):
        result = await self.mongo_client.InsertByKeyValue(
            "user_content", "postings", self.query
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

    async def u_get_plist(self, username):
        user = await self.u_get(username)
        return user['postings']



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
