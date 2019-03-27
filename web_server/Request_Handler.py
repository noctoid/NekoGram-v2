#!/usr/bin/python3.7
import asyncio
from uuid import uuid4
from Q_Connector import AsyncPersistenceConnector
from Models import Posting, User
from settings import Q_API_VER
import json

class RequestHandler:
    def __init__(self):
        self.ODM = None

    async def _initialize(self, loop):
        self.ODM = await AsyncPersistenceConnector(loop).connect()

    async def exec(self, method, payload):
        if not self.ODM:
            await self._initialize(asyncio.get_event_loop())
        return await self.ODM.call({"method": method, "payload": payload})

    async def auth_user(self, username, password):
        payload = {
            "username": username,
            "password": password
        }
        return await self.exec("u.auth", payload)

    async def get_postings(self, pid):
        # aio_db = await AsyncPersistenceConnector(asyncio.get_event_loop()).connect()
        payload = {
            'list_of_pid': [pid]
        }
        return await self.exec("p.get", payload)

    async def get_postings_batch(self, list_of_pid):
        payload = {
            "list_of_pid": list_of_pid
        }
        return await self.exec("p.get", payload)

    async def update_postings(self, pid, modification):
        return await self.exec(
            "p.update",
            {
                "pid": pid,
                'modification':modification
            }
        )

    async def delete_postings(self, pid):
        return await self.exec("p.remove", {"list_of_pid":[pid]})

    async def create_postings(self, P:Posting):
        payload = {"new_post": P.to_dict()}
        # return await self.exec("p.new", payload)
        result = await self.exec("p.new", payload)
        result = json.loads(result)['result']
        print("shenmejiba", result)
        status, new_pid, uid = result['status'], result['pid'], P.get_uid()
        update_user_result = await self.update_user(uid, {"postings":new_pid})
        print("!!!!",update_user_result)

        return {"status": 200, "message": "success"}

    async def create_user(self, U:User):
        payload = {"new_user": U.to_dict()}
        return await self.exec("u.new", payload)

    async def get_user(self, username):
        payload = {"username": username} #nickname for now change later
        return await self.exec("u.get", payload)

    async def list_user_postings(self, username):
        payload = {
            "username": username
        }
        return await self.exec("u.get_plist", payload)

    async def update_user(self, uid, modification):
        payload = {
            "uid": uid,
            "modification": modification
        }
        return await self.exec("u.update", payload)

    async def update_user_postings(self, uid, modification):
        payload = {
            "uid": uid,
            "modification": modification
        }
        return await self.exec("u.update_postings", payload)


    async def delete_user(self, uid):
        return await self.exec("u.remove", {"list_of_uid": [uid]})