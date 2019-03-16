import boto3
from botocore.client import Config
from uuid import uuid4
from base64 import b64decode
import imghdr

class file_like_obj:
    def __init__(self, bytes_in_b64):
        self.stream = b64decode(bytes_in_b64)

    def read(self, *args, **kwargs):
        return self.stream

def _what_file(bytes):
    if imghdr.test_bmp(bytes, 0) == "bmp":
        return "bmp"
    elif imghdr.test_gif(bytes, 0) == "gif":
        return "gif"
    elif imghdr.test_jpeg(bytes, 0) == "jpeg":
        return "jpeg"
    elif imghdr.test_webp(bytes, 0) == "webp":
        return "webp"
    elif imghdr.test_png(bytes, 0) == 'png':
        return 'png'


async def new_media(s3, media_id, bytes_in_b64):
    fileLikeObj = file_like_obj(bytes_in_b64)
    suffix = _what_file(fileLikeObj.read())
    if suffix:
        file_key = media_id + "." + suffix
        s3.Bucket("media").upload_fileobj(fileLikeObj, file_key, ExtraArgs={"ACL": "public-read"})
        return "http://169.254.146.101:9000/media/"+file_key

def remove_media(media_key):
    pass


# uid = str(uuid4())
# s3.Bucket('images').upload_file('/home/yoko/Pictures/1.png', uid+'.png', ExtraArgs={"ACL": "public-read"})
#
# with open("index.html", "w") as f:
# 	f.write("<img src=\"http://10.0.1.223/images/"+uid+".png\"></img>")
#
# print("done.")

if __name__ == "__main__":
    s3 = boto3.resource("s3",
                        endpoint_url="http://169.254.146.101:9000",
                        config=Config(signature_version='s3v4'),
                        region_name='us-east-1')

    from base64 import b64encode
    with open('nanpu.JPG', 'rb') as f:
        b = b64encode(f.read())
    src = new_media(s3, str(uuid4()), b)
    with open("index.html", "w") as f:
        f.write("<img src=\""+src+"\"></img>")