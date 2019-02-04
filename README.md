# NekoGram-v2
NekoGram Version 2

## Web Server

NekoGram web server is built on the great Python web framework Sanic which supports async/await functions that vastly increase the performance of any web app built using it. 

## Front End App

NekoGram Frontend App is an single page javascript application written in React.

## Database Wrapper

To ensure maximum data access throughput, the Database Wrapper is designed to listen RPC calls from RabbitMQ, and fetch the command from the containing json.

API:
```
{
    "db": "postings",
    "query" : {
        "method": "read",
        "posting-id": 123456789
    }
}
```

Data retrieved will be in form of certain object also packed in json.

