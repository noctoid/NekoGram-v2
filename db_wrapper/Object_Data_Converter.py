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
        elif self.obj == "comments":
            pass
        elif self.obj == "likes":
            pass

    # All read methods
    async def get_postings(self):
        result = await self.mongo_client.findByKeyValue(
            "user-content", "postings",
            self.query["key"], self.query["value"]
        )
        return result


    # All write methods
    async def create_postings(self):
        payload = self.query['payload']
        result = await self.mongo_client.InsertByKeyValue(
            "user-content", "postings", {}
        )
        return {"status": 200}


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
