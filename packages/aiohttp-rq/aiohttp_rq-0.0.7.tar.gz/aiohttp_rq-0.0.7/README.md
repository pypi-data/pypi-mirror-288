### Installation
```bash
$ pip install aiohttp-rq
```

### Environment variables
Variable|default
-|-
`AIOHTTP_RQ_DIR`|`None`
`AIOHTTP_RQ_REQUEST_QUEUE`|`aiohttp-rq-request`
`AIOHTTP_RQ_RESPONSE_QUEUE`|`aiohttp-rq-response`
`AIOHTTP_RQ_EXCEPTION_QUEUE`|`aiohttp-rq-exception`

optional
Variable|default
-|-
`AIOHTTP_RQ_LOG_CONFIG_FILE`|`None`
`AIOHTTP_RQ_TTL_DNS_CACHE`|`10`
`REDIS_HOST`|`localhost`
`REDIS_PORT`|`6379`
`REDIS_DB`|`0`

### Features
+   logging
    +   `DEBUG`, `ERROR` level messages
    +   `logging.conf` support: `AIOHTTP_RQ_LOG_CONFIG_FILE`
+   request data: `method`,`url`, `headers`, `data`,`allow_redirects`, custom arguments
+   response data: `url`, `status`, `headers`,`content_path`, `request_xxx` arguments
+   request exception data: `url`, `exc_class`, `exc_message`, `request_xxx` arguments

### Examples
```bash
$ export AIOHTTP_RQ_REQUEST_QUEUE="aiohttp-rq-request"
$ export AIOHTTP_RQ_RESPONSE_QUEUE="aiohttp-rq-response"
$ export AIOHTTP_RQ_EXCEPTION_QUEUE="aiohttp-rq-exception"
$ export AIOHTTP_RQ_TTL_DNS_CACHE=3600 # optional
$ python3 -m aiohttp_rq 50 # 50 workers

```

redis client
```python
import redis

REDIS = redis.Redis(host='localhost', port=6379, db=0)
```

#### Redis push

```python
value=json.dumps(dict(
    url='https://domain.com',
    method="GET",
    headers=None,
    data=None,
    allow_redirects=True
))
REDIS.rpush('aiohttp-rq-request',*values)
```

#### Redis pull

```python
item_list = REDIS.lrange('aiohttp-rq-response',0,-1)
for item in item_list:
    data = json.loads(item.encode('utf-8'))

item_list = REDIS.lrange('aiohttp-rq-exception',0,-1)
for item in item_list:
    data = json.loads(item.encode('utf-8'))
```

