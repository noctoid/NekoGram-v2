#!/usr/bin/python3
import asyncio
from motor import motor_asyncio
from pprint import pprint

class Async_Mongo_Connector:
    def __init__(self, ip="127.0.0.1", port="27017", login="", password=""):
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password

        self.client = motor_asyncio.AsyncIOMotorClient(self.ip)
        print(self.client)

    async def mockup(self):
        return {"test": "result", "success": 233}

    async def findByKeyValue(self, db, colle, key, value):
        # return a list of found document
        doc = await self.client[db][colle].find_one({key:value})
        return doc

    async def InsertByKeyValue(self, db, colle, doc):
        status = await self.client[db][colle].insert_one(doc)
        return status

    async def updateByKeyValue(self, db, colle, key, value, modification):
        status = await self.client[db][colle].find_one_and_update({key:value}, {"$set": modification})
        return status

    async def deleteByKeyValue(self, db, colle, key, value):
        status = await self.client[db][colle].find_one_and_delete({key: value})
        return status

if __name__ == "__main__":
    c = Async_Mongo_Connector()
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(c.mockup)
    result = loop.run_until_complete(c.findByKeyValue("user_content","postings", "post-id", 1234567))
    pprint(result)