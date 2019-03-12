#!/usr/bin/python3
import asyncio


# from mongodb_connector import Async_Mongo_Connector


class OD_Converter:
    # def __init__(self, db, obj_requested=None, method=None, query=None):
    def __init__(self, db_connection):
        try:
            # self.mongo_client = Async_Mongo_Connector()
            self.mongo_client = db_connection
            # self.obj = obj_requested
            # self.method = method
            # self.query = query
        except:
            raise ConnectionError

    def load(self, obj, method, query):
        """
        :param obj:     "postings", "comments", "likes"
        :param method:  "read", "delete", "update", "create"
        :param query:   depend on query
        :return:
        """
        self.obj = obj
        self.method = method
        self.query = query

    async def do(self):
        """
        :return:
        """
        if self.obj == "postings":
            if self.method == "read":
                return await self.p_read()
            elif self.method == "create":
                return await self.p_new()
            elif self.method == "update":
                return await self.p_update()
            elif self.method == "delete":
                return await self.p_remove()
            elif self.method == "batch_read":
                return await self.batch_get_postings()
            elif self.method == "u_get_plist":
                return await self.u_get_plist()
        elif self.obj == "comments":
            pass
        elif self.obj == "likes":
            pass
        elif self.obj == "profiles":
            if self.method == "create":
                return await self.u_new()
            elif self.method == "read":
                return await self.u_get()
            elif self.method == "checkpwd":
                return await self.auth_user()

    async def u_auth(self, username, password):
        user = await self.u_get(username)
        print(user)
        if not user:
            return {"status": "failed", "message": "No such user"}
        return {"status": "success", "auth": user['password'] == password}

    # All read methods
    # async def p_get(self):
    #     result = await self.mongo_client.findByKeyValue(
    #         "user_content", "postings",
    #         self.query["key"], self.query["value"]
    #     )
    #     return result

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
