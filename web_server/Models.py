from uuid import uuid4
import json

class User:
    def __init__(self, user_id= "",uid="", password="", username="", displayName="", profile_image=None):
        self.user_id = user_id
        self.uid = uid
        if not uid:
            self.uid = str(uuid4())
        self.email = ""
        self.phone = ""
        self.password = password
        self.username = username
        self.displayName = displayName
        self.postings = []
        self.following = []
        self.followers = []
        self.notifications = []
        self.profile_image = profile_image

    def __repr__(self):
        return "NekoGram User: "+self.uid+self.displayName+self.username

    def to_dict(self):
        return {
            "user_id": self.uid,
            "uid": self.uid,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
            "username": self.username,
            "displayName": self.displayName,
            "postings": self.postings,
            "following": self.following,
            "followers": self.followers,
            "notifications": self.notifications,
            "profile_image": self.profile_image,
        }

    def json(self):
        return json.dumps(self.to_dict())

    def isValid(self, api):
        pass

class Posting:
    def __init__(
            self,
            pid="", uid="", type="", content={},
            comments=[], likes=[], repost=[], public=True
            ):
        self.p = {}
        self.p["uid"] = uid
        self.p["type"] = type
        self.p["comments"] = comments
        self.p["likes"] = likes
        self.p["repost"] = repost
        self.p["public"] = public
        self.p["content"] = content
        if pid:
            self.p["pid"] = pid
        else:
            self.p["pid"] = str(uuid4())

    def __repr__(self):
        try:
            return " ".join(
                [
                    "Posting:", "p:",self.p["pid"],
                    "u:",self.p["uid"]
                ])
        except:
            return "Posting: Invalid"

    def to_dict(self):
        return self.p

    def json(self):
        return json.dumps(self.to_dict())

    def get_pid(self):
        return self.p["pid"]

    def get_uid(self):
        return self.p["uid"]



if __name__ == "__main__":
    from pprint import pprint as pp
    posting = Posting(uid=str(uuid4()), type="posting", content={"txt": "test!"})
    print(posting)
    pp(posting.to_dict())
    print(posting.get_uid())
    print(posting.json())
