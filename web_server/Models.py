from uuid import uuid4
import json

class User:
    def __init__(self, username="", password="", permission=""):
        self.username = username
        self.password = password
        self.permission = permission

    def __repr__(self):
        return "NekoGram User: "+self.username+self.permission

    def isValid(self, api):
        pass

class Posting:
    def __init__(self, pid = "", uid="", txt="", mime="", media_url="", valid=True, comments="", likes=""):
        self.uid = uid
        self.txt = txt
        self.mime = mime
        self.media_url = media_url
        self.valid = valid
        if comments:
            self.comments = comments
        else:
            self.comments = str(uuid4())
        if likes:
            self.likes = likes
        else:
            self.likes = str(uuid4())
        if pid:
            self.pid = pid
        else:
            self.pid = str(uuid4())

    def __repr__(self):
        try:
            return " ".join(
                [
                    "Posting:", "p:",self.pid,
                    "u:",self.uid
                ])
        except:
            return "Posting: Invalid"

    def to_dict(self):
        return {
            "pid": self.pid,
            "uid": self.uid,
            "mime": self.mime,
            "media_url": self.media_url,
            "valid": self.valid,
            "comments": self.comments,
            "likes": self.likes
        }

    def json(self):
        return json.dumps(self.to_dict())

    def isValid(self):
        return self.valid

class Like:
    pass

class Comment:
    pass


if __name__ == "__main__":
    from pprint import pprint as pp
    posting = Posting(uid=str(uuid4()), txt="Hi Posting", mime="", media_url="")
    print(posting)
    pp(posting.to_dict())
    print(posting.json())
