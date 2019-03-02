#!/usr/bin/python3.7
import asyncio
from uuid import uuid4
from Q_Connector import AsyncPersistenceConnector
from settings import Q_API_VER

class RequestHandler:
    def __init__(self):
        self.sample_query = {
            "ver": Q_API_VER,
            "object": "",
            "method": "",
            "query": {}
        }

        self.sample_postings = {
            "pid": "",
            "uid": "",
            "txt": "",
            "media-mime": "",
            "media-url": [""]
        }
        self.ODM = None

    async def _initialize(self, loop):
        self.ODM = await AsyncPersistenceConnector(loop).connect()


    async def get_postings(self, key, value):
        # aio_db = await AsyncPersistenceConnector(asyncio.get_event_loop()).connect()
        query = self.sample_query
        query["object"] = "postings"
        query["method"] = "read"
        query["query"] = {
            "key": key,
            "value": value
        }
        # result = await aio_db.call(query)
        # await aio_db.close()
        if not self.ODM:
            await self._initialize(asyncio.get_event_loop())
        result = await self.ODM.call(query)

        return result


    async def create_postings(self, uid, txt, mime, media_url):
        doc = {
            "uid": uid,
            "pid": str(uuid4()),
            "txt": txt,
            "mime": mime,
            "media_url": media_url
        }
        aio_db = await AsyncPersistenceConnector(asyncio.get_event_loop()).connect()
        query = self.sample_query
        query["object"] = "postings"
        query["method"] = "create"
        query["query"] = doc
        # result = await aio_db.call(query)
        # await aio_db.close()
        if not self.ODM:
            await self._initialize(asyncio.get_event_loop())
        result = await self.ODM.call(query)

        return result