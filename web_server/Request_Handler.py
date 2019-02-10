#!/usr/bin/python3.7
import asyncio
from Q_Connector import AsyncPersistenceConnector
from settings import Q_API_VER

class RequestHandler:
    def __init__(self):
        self.read_query = {
            "ver": Q_API_VER,
            "object": "",
            "method": "read",
            "query": {
                "key": "",
                "value": 0
            }
        }


    async def get_postings(self, key, value):
        aio_db = await AsyncPersistenceConnector(asyncio.get_event_loop()).connect()
        query = self.read_query
        query["object"] = "postings"
        query["method"] = "read"
        query["query"] = {
            "key": key,
            "value": value
        }
        result = await aio_db.call(query)
        await aio_db.close()
        return result


    async def create_postings(self):
        aio_db = await AsyncPersistenceConnector(asyncio.get_event_loop()).connect()
        result = await aio_db.call({
            "ver": "0.1",
            "object": "postings",
            "method": "create",
            "query": {
                "pid": 1234568,
                "uid": 1234567,
                "txt": "I have pineapple"
            }
        })
        await aio_db.close()
        return result