# NekoGram-v2
NekoGram Version 2

## Web Server

NekoGram web server is built on the great Python web framework Sanic which supports async/await functions that vastly increase the performance of any web app built using it.

### API
##### postings
All postings related APIs are like this /p/... 

```html
/p/get/
/p/create/
/p/delete/
/p/update/
```
##### comments
```html
/c/get/
/c/create/
/c/delete/
/c/update/
```
##### likes 
```html
/l/get/
/l/do/
/l/undo/
```

## Front End App

NekoGram Frontend App is an single page javascript application written in React.

## Database Wrapper

To ensure maximum data access throughput, the Database Wrapper is designed to listen RPC calls from RabbitMQ, and fetch the command from the containing json.

Sample Postings Related Requests:
```json
{
    "ver": "0.1",
    "object": "postings",
    "method": "read",
    "query" : {
        "payload": {
          "posting-id": 123456789,
          "user-id": "..."
        }
    }
}
```
```json
{
    "ver": "0.1",
    "object": "postings",
    "method": "delete",
    "query" : {
        "payload": {
          "posting-id": 123456789,
          "user-id": "..."
        }
    }
}
```
```json
{
    "ver": "0.1",
    "object": "postings",
    "method": "update",
    "query" : {
        "payload": {
            "posting-id": 123456789,
            "user-id": "...",
            "text": "blahblahblah...",
            "media-mime": "image/jpg",
            "media-url": "https://example.com/image/s123456789"
        }
    }
}
```
```json
{
    "ver": "0.1",
    "object": "postings",
    "method": "create",
    "query" : {
        "payload": {
            "posting-id": 123456789,
            "user-id": "...",
            "text": "blahblahblah...",
            "media-mime": "image/jpg",
            "media-url": "https://example.com/image/s123456789"
        }
    }
}
```
Sample Comments Requests:
Create comment
```json
{
    "ver": "0.1",
    "object": "comments",
    "method": "create",
    "query": {
        "payload": {
            "posting-id": 123456789,
            "user-id": "...",
            "comment-id": "...",
            "text": "blahblahblah...."
        }
    }
}
```
Delete comment
```json
{
    "ver": "0.1",
    "object": "comments",
    "method": "delete",
    "query": {
        "method": "delete",
        "payload": {
            "posting-id": 123456789,
            "user-id": "...",
            "comment-id": "..."
        }
    }
}
```

Sample Likes Requests:
Like
```json
{
  "ver": "0.1",
  "object": "likes",
  "method": "create",
  "query": {
    "payload": {
      "posting-id": 123456789,
      "user-id": "..."
    }
  }
}
```
Dislike
```json
{
  "ver": "0.1",
  "object": "likes",
  "method": "delete",
  "query": {
    "payload": {
      "posting-id": 123456789,
      "user-id": "..."
    }
  }
}
```

Data retrieved will be in form of certain object also packed in json.


## Information Experts

All the data models are described in this session, and they are ```User, Posting, Like, Comment, Notification```.

#### User

```json
{
  "uid": "uuid4",
  "email": "schrodinger@example.com",
  "phone": "+11234567890",
  "password": "hash_of_the_password",
  "username": "username",
  "displayName": "Display Name",
  "profile_image": "https://cdn.example.com/img/1234567.png",
  "postings": [
    "pid-1", "pid-2", "..."
  ],
  "notification": [
    {
      "nid": "1234",
      "etc": "..."
    }, {}
  ]
  
}

```

#### Posting
There are 4 types of postings which are differentiated by ```type``` attribute; and they are 
```posting```, ```like```, ```comment```, ```repost``` which have different content.
```json
// Meta Posting
{
  "pid": "uuid4-0000-0000-0000-00000000",
  "uid": "uuid4-9999-1234-5678-12345678",
  "type": "posting", // or "like", "comment", "repost"
  "content": {...}   // actual content
  "comments": [ // list of pid
    "uuid4-0000-0000-0000-00000001",
    "..."
   ],
   "likes": [ // list of pid
    "uuid4-0000-0000-0000-00000004",
    "..."
   ],
   "repost": [
    "uuid4-0000-0000-0000-00000007",
    "..."
   ],
   "scope": "public" // or "friend", or "self"
}
```
Posting Content:
Posting Content contains text and media
```json
{
  "txt": "I had In n Out for lunch today and it is good.",
  "hasMedia": true,
  "mimeType": "image/png",
  "mediaUrl": "https://cdn.example.com/img/a-nice-burger.png",
  
}
```

Likes Content: 
Likes has no real content, but the ```pid``` of the posting it likes.
```json
{
  "target_pid": "uuid4-0000-1111-2222-00000000"
}
```

Repost Content:
Repost has a quote (may be empty) and the ```pid``` of the posting
```json
{
  "target_pid": "uuid4-0000-1111-2222-00000000",
  "txt": "Nice Post!"
}
```

Comment Content:
Repost has a quote (cannot be empty) and the ```pid``` of the posting
```json
{
  "target_pid": "uuid4-0000-1111-2222-00000000",
  "txt": "Good job!"
}
```

