#!/usr/bin/python3
import asyncio
# from mongodb_connector import Async_Mongo_Connector


class Retriever:
    def __init__(self, db):
        try:
            # self.mongo_client = Async_Mongo_Connector()
            self.mongo_client = db
            self.obj = None
            self.method = None
            self.query = None
        except:
            raise ConnectionError

    def load(self, obj, method, query):
        self.obj = obj
        self.method = method
        self.query = query

    async def do(self):
        if self.method == "read":
            return await self.get_postings()
        elif self.method == "create":
            return await self.create_postings()


    async def get_postings(self):
        result = await self.mongo_client.findByKeyValue(
            "user-content", "postings",
            "post-id", self.query["payload"]["post-id"]
        )
        return result

    async def create_postings(self):
        payload = self.query['payload']
        result = await self.mongo_client.InsertByKeyValue(
            "user-content", "postings", {}
        )
        return {"status": 200}

if __name__ == "__main__":
    c = Retriever()
    loop = asyncio.get_event_loop()
    c.load("postings", "read", {
        "payload": {
            "posting-id": 1234567
        }
    })
    result = loop.run_until_complete(c.get_postings())

    print(result)