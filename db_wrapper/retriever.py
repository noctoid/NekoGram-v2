#!/usr/bin/python3
import asyncio
from mongodb_connector import Async_Mongo_Connector


class Retriever:
    def __init__(self):
        try:
            self.mongo_client = Async_Mongo_Connector()
        except:
            raise ConnectionError

    def load(self, obj, method, query):
        self.obj = obj
        self.method = method
        self.query = query


    async def get_posting_by_id(self):
        result = await self.mongo_client.findByKeyValue(
            "user-content", "postings",
            "post-id", self.query["payload"]["posting-id"]
        )
        return result

if __name__ == "__main__":
    c = Retriever()
    loop = asyncio.get_event_loop()
    c.load("postings", "read", {
        "payload": {
            "posting-id": 1234567
        }
    })
    result = loop.run_until_complete(c.get_posting_by_id())

    print(result)