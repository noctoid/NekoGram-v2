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
    "object": "postings",
    "query" : {
        "method": "read",
        "posting-id": 123456789,
        "payload": {
          "user-id": "..."
        }
    }
}
```
```json
{
    "object": "postings",
    "query" : {
        "method": "delete",
        "posting-id": 123456789,
        "payload": {
          "user-id": "..."
        }
    }
}
```
```json
{
    "object": "postings",
    "query" : {
        "method": "update",
        "posting-id": 123456789,
        "payload": {
            "user-id": "...",
            "text": "blahblahblah...",
            "media-mime": "image/jpg",
            "media-url": "https://example.com/image/s123456789",
        }
    }
}
```
```json
{
    "object": "postings",
    "query" : {
        "method": "create",
        "posting-id": 123456789,
        "payload": {
            "user-id": "...",
            "text": "blahblahblah...",
            "media-mime": "image/jpg",
            "media-url": "https://example.com/image/s123456789"
        }
    }
}
```
Sample Comments Requests:
```json
{
    "object": "comments",
    "query": {
        "method": "create",
        "posting-id": 123456789,
        "payload": {
            "user-id": "...",
            "text": "blahblahblah...."
        }
    }
}
```

Sample Likes Requests:
Like
```json
{
  "object": "likes",
  "query": {
    "method": "create",
    "posting-id": 123456789,
    "payload": {
      "user-id": "..."
    }
  }
}
```
Dislike
```json
{
  "object": "likes",
  "query": {
    "method": "delete",
    "posting-id": 123456789,
    "payload": {
      "user-id": "..."
    }
  }
}
```

Data retrieved will be in form of certain object also packed in json.

