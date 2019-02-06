# NekoGram-v2
NekoGram Version 2

## Web Server

NekoGram web server is built on the great Python web framework Sanic which supports async/await functions that vastly increase the performance of any web app built using it. 

## Front End App

NekoGram Frontend App is an single page javascript application written in React.

## Database Wrapper

To ensure maximum data access throughput, the Database Wrapper is designed to listen RPC calls from RabbitMQ, and fetch the command from the containing json.

Sample Postings Related Requests:
```json
{
    "ver": 1,
    "object": "postings",
    "query" : {
        "method": "read",
        "payload": {
          "posting-id": 123456789,
          "user-id": "..."
        }
    }
}
```
```json
{
    "ver": 1,
    "object": "postings",
    "query" : {
        "method": "delete",
        "payload": {
          "posting-id": 123456789,
          "user-id": "..."
        }
    }
}
```
```json
{
    "ver": 1,
    "object": "postings",
    "query" : {
        "method": "update",
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
    "ver": 1,
    "object": "postings",
    "query" : {
        "method": "create",
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
    "ver": 1,
    "object": "comments",
    "query": {
        "method": "create",
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
    "ver": 1,
    "object": "comments",
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
  "ver": 1,
  "object": "likes",
  "query": {
    "method": "create",
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
  "ver": 1,
  "object": "likes",
  "query": {
    "method": "delete",
    "payload": {
      "posting-id": 123456789,
      "user-id": "..."
    }
  }
}
```

Data retrieved will be in form of certain object also packed in json.

