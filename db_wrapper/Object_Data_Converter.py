#!/usr/bin/python3
import asyncio


# from mongodb_connector import Async_Mongo_Connector


class OD_Converter:
    def __init__(self, db, obj_requested=None, method=None, query=None):
        try:
            # self.mongo_client = Async_Mongo_Connector()
            self.mongo_client = db
            self.obj = obj_requested
            self.method = method
            self.query = query
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
                return await self.get_postings()
            elif self.method == "create":
                return await self.create_postings()
            elif self.method == "update":
                return await self.update_postings()
            elif self.method == "delete":
                return await self.delete_postings()
            elif self.method == "batch_read":
                return await self.batch_get_postings()
            elif self.method == "user_plist":
                return await self.user_plist()
        elif self.obj == "comments":
            pass
        elif self.obj == "likes":
            pass
        elif self.obj == "profiles":
            if self.method == "create":
                return await self.create_user()
            elif self.method == "read":
                return await self.get_user()

    # All read methods
    async def get_postings(self):
        result = await self.mongo_client.findByKeyValue(
            "user_content", "postings",
            self.query["key"], self.query["value"]
        )
        return result

    async def batch_get_postings(self):
        result = []
        for q in self.query["list_of_pid"]:
            elem = await self.mongo_client.findByKeyValue(
                "user_content", "postings",
                "pid", q
            )
            elem.pop("_id")
            result.append(elem)
        print("DB->", result)
        return result

    async def user_plist(self):
        self.query['key'] = "uid"
        self.query['value'] = self.query["uid"]
        user = await self.get_user()
        return user['postings']



    # All write methods
    async def create_postings(self):
        result = await self.mongo_client.InsertByKeyValue(
            "user_content", "postings", self.query
        )
        return {"status": 200}

    async def create_user(self):
        isUserExist = await self.mongo_client.findByKeyValue(
            "user_content", "profiles", "username", self.query["username"]
        )
        if isUserExist:
            return {"status": 403, "message": "username taken"}
        result = await self.mongo_client.InsertByKeyValue(
            "user_content", "profiles", self.query
        )
        return {"status": 200}

    async def get_user(self):
        result = await self.mongo_client.findByKeyValue(
            "user_content", "profiles", self.query['key'], self.query['value']
        )
        return result


if __name__ == "__main__":
    c = OD_Converter()
    loop = asyncio.get_event_loop()
    c.load("postings", "read", {
        "payload": {
            "posting-id": 1234567
        }
    })
    result = loop.run_until_complete(c.get_postings())

    print(result)
