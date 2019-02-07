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

