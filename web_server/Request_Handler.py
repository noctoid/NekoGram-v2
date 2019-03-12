#!/usr/bin/python3.7
import asyncio
from uuid import uuid4
from Q_Connector import AsyncPersistenceConnector
from Models import Posting, User
from settings import Q_API_VER

class RequestHandler:
    def __init__(self):
        self.sample_query = {
            "ver": Q_API_VER,
            "object": "",
            "method": "",
            "query": {}
        }

        self.ODM = None

    async def _initialize(self, loop):
        self.ODM = await AsyncPersistenceConnector(loop).connect()

    async def exec(self, query):
        if not self.ODM:
            await self._initialize(asyncio.get_event_loop())
        return await self.ODM.call(query)

    async def auth_user(self, username, password):
        query = self.sample_query
        query["object"] = "profiles"
        query["method"] = "checkpwd"
        query["query"] = {
            "username": username,
            "password": password
        }

        return await self.exec(query)

    async def get_postings(self, key, value):
        # aio_db = await AsyncPersistenceConnector(asyncio.get_event_loop()).connect()
        query = self.sample_query
        query["object"] = "postings"
        query["method"] = "read"
        query["query"] = {
            "key": key,
            "value": value
        }
        return await self.exec(query)

    async def get_postings_batch(self, list_of_pid):
        query = self.sample_query
        query["object"] = "postings"
        query["method"] = "batch_read"
        query['query'] = {
            "list_of_pid": list_of_pid
        }
        return await self.exec(query)

    async def list_user_postings(self, uid):
        query = self.sample_query
        query["object"] = "postings"
        query["method"] = "u_get_plist"
        query["query"] = {
            "uid": uid
        }
        return await self.exec(query)

    async def create_postings(self, uid, txt, mime, media_url):
        doc = {
            "uid": uid,
            "pid": str(uuid4()),
            "txt": txt,
            "mime": mime,
            "media_url": media_url
        }
        # aio_db = await AsyncPersistenceConnector(asyncio.get_event_loop()).connect()
        query = self.sample_query
        query["object"] = "postings"
        query["method"] = "create"
        query["query"] = doc
        return await self.exec(query)

    async def create_postings_2(self, P:Posting):
        query = self.sample_query
        query["object"] = "postings"
        query["method"] = "create"
        query["query"] = P.to_dict()
        return await self.exec(query)

    async def create_user(self, U:User):
        query = self.sample_query
        query['object'] = 'profiles'
        query['method'] = 'create'
        query['query'] = U.to_dict()
        return await self.exec(query)

    async def get_user(self, username):
        query = self.sample_query
        query["object"] = "profiles"
        query["method"] = "read"
        query["query"] = {"key": "username", "value": username} #nickname for now change later
        return await self.exec(query)