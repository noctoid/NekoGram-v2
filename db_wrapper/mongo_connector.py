#!/usr/bin/python3
from pymongo import MongoClient


class MongoDB_Connector:
    def __init__(self, ip="127.0.0.1", port="27017", username="", password=""):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

        self.client = MongoClient("mongodb://" + ip + ":" + port)

    def mockup(self):
        return {"test": "result", "success": 233}

    def findByKeyValue(self, db, colle, key, value):
        # return a list of found document
        return [doc["content"] for doc in self.client[db][colle].find({key: value})]