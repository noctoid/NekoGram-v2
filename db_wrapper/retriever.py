#!/usr/bin/python3
import asyncio
from mongodb_connector import Async_Mongo_Connector


class Retriever:
    def __init__(self):
        try:
            self.mongo_client = Async_Mongo_Connector()
        except:
            raise ConnectionError


    async def get_posting_by_id(self, query):
        result = await self.mongo_client.findByKeyValue(
            "user-content", "postings",
            "post-id", query["payload"]["posting-id"]
        )
        return result

if __name__ == "__main__":
    c = Retriever()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(c.get_posting_by_id({
        "method": "read",
        "payload": {
            "posting-id": 1234567
        }
    }))

    print(result)