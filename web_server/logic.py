#!/usr/bin/python3.7
import asyncio
from connector_base import AsyncPersistenceConnector
from settings import Q_API_VER

class Logic:
    def __init__(self):
        pass


    async def get_postings(self):
        aio_db = await AsyncPersistenceConnector(asyncio.get_event_loop()).connect()
        result = await aio_db.call({
            "ver": "0.1",
            "object": "postings",
            "method": "read",
            "query": {
                "payload": {
                    "post-id": 1234567,
                }
            }
        })
        await aio_db.close()
        return result


    async def create_postings(self):
        aio_db = await AsyncPersistenceConnector(asyncio.get_event_loop()).connect()
        result = await aio_db.call({
            "ver": "0.1",
            "object": "postings",
            "method": "create",
            "query": {
                "payload": {
                    "post-id": 1234568,
                    "user-id": 1234567,
                    "text": "I have pineapple"
                }
            }
        })
        await aio_db.close()
        return result