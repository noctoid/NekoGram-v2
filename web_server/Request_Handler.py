#!/usr/bin/python3.7
import asyncio
from uuid import uuid4
from Q_Connector import AsyncPersistenceConnector
from Models import Posting, User
from settings import Q_API_VER

class RequestHandler:
    def __init__(self):
        self.sample_query = {
            "method": "",
            "payload": {}
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
        query["method"] = "u.auth"
        query["payload"] = {
            "username": username,
            "password": password
        }

        return await self.exec(query)

    async def get_postings(self, pid):
        # aio_db = await AsyncPersistenceConnector(asyncio.get_event_loop()).connect()
        query = self.sample_query
        query["method"] = "p.get"
        query["payload"] = {
            'list_of_pid': [pid]
        }
        return await self.exec(query)

    async def get_postings_batch(self, list_of_pid):
        query = self.sample_query
        query["method"] = "p.get"
        query['payload'] = {
            "list_of_pid": list_of_pid
        }
        return await self.exec(query)

    async def list_user_postings(self, username):
        query = self.sample_query
        query["method"] = "u.get_plist"
        query["payload"] = {
            "username": username
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
        query = self.sample_query
        query["method"] = "create"
        query["payload"] = {"new_post": doc}
        return await self.exec(query)

    async def create_postings_2(self, P:Posting):
        query = self.sample_query
        query["method"] = "p.new"
        query["payload"] = {"new_post": P.to_dict()}
        return await self.exec(query)

    async def create_user(self, U:User):
        query = self.sample_query
        query['method'] = 'u.new'
        query['payload'] = {"new_user": U.to_dict()}
        return await self.exec(query)

    async def get_user(self, username):
        query = self.sample_query
        query["method"] = "u.get"
        query["payload"] = {"username": username} #nickname for now change later
        return await self.exec(query)