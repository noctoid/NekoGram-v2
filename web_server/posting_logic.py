#!/usr/bin/python3.7
import asyncio
from connector_base import AsyncPersistenceConnector


async def get_postings():
    aio_db = await AsyncPersistenceConnector(asyncio.get_event_loop()).connect()
    result = await aio_db.call({
        "ver": "0.1",
        "object": "postings",
        "method": "read",
        "query": {
            "payload": {
                "posting-id": 1234567,
            }
        }
    })
    return result