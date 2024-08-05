import asyncio
import json
import logging
import logging.config
import os
import sys
import time

import aiohttp
import click
import redis

from .utils import get_client_session_kwargs, get_content_path, write_content

if os.path.exists('logging.conf'):
    logging.config.fileConfig('logging.conf')

REDIS_PREFETCH_COUNT = 100
ASYNCIO_REQUEST_QUEUE = asyncio.Queue()
# https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.request
REQUEST_KEYS = ['method','url','params','data','json','headers','cookies','allow_redirects','compress','chunked','expect100',]

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
REDIS = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

REQUEST_QUEUE_NAME = os.getenv("AIOHTTP_RQ_REQUEST_QUEUE", "aiohttp_rq_request")
RESPONSE_QUEUE_NAME = os.getenv("AIOHTTP_RQ_RESPONSE_QUEUE", "aiohttp_rq_response")
REQUEST_EXCEPTION_QUEUE_NAME = os.getenv("AIOHTTP_RQ_REQUEST_EXCEPTION_QUEUE", "aiohttp_rq_request_exception")

async def redis_queue_worker(session):
    global ASYNCIO_REQUEST_QUEUE
    while True:
        try:
            pipe = REDIS.pipeline()
            pipe.lrange(REQUEST_QUEUE_NAME, 0, REDIS_PREFETCH_COUNT - 1)
            pipe.ltrim(REQUEST_QUEUE_NAME, REDIS_PREFETCH_COUNT, -1)
            value_list, trim_success = pipe.execute()
            if not value_list:
                await asyncio.sleep(0.1)
                continue
            for value in value_list:
                data = json.loads(value.decode("utf-8"))
                await ASYNCIO_REQUEST_QUEUE.put(data)
        except Exception as e:
            logging.error(e)
            sys.exit(1)

async def request_worker(session):
    global ASYNCIO_REQUEST_QUEUE
    while True:
        try:
            data = await ASYNCIO_REQUEST_QUEUE.get()
            url, method = data['url'], data['method']
            kwargs = {k:data[k] for k in data.keys() if k in REQUEST_KEYS}
            if isinstance(kwargs.get('data',None),dict):
                kwargs['data'] = json.dumps(kwargs['data'])
            logging.debug('%s %s' % (method,url))
        except Exception as e:
            logging.error(e)
            sys.exit(1)
        try:
            async with session.request(**kwargs) as r:
                logging.debug('STATUS %s %s' % (url,r.status))
                content_path = None
                if method.upper()!='HEAD' and r.status not in [404]:
                    content_path = get_content_path()
                    logging.debug('WRITE %s -> %s' % (url,content_path))
                    await write_content(r,content_path)
                queue = RESPONSE_QUEUE_NAME
                push_data = dict(
                    url=str(r.url),
                    status=int(r.status),
                    headers = dict(r.headers),
                    content_path=content_path,
                    **{'request_%s' % k:v for k,v in data.items()}
                )
        except Exception as e: # session.request() exception
            logging.debug('%s %s: %s' % (url,type(e),str(e)))
            queue = REQUEST_EXCEPTION_QUEUE_NAME
            push_data = dict(
                url=url,
                exc_class="%s.%s" % (type(e).__module__, type(e).__name__),
                exc_message=str(e),
                **{'request_%s' % k:v for k,v in data.items()}
            )
        try:
            logging.debug('REDIS PUSH: %s' % queue)
            REDIS.rpush(queue, json.dumps(push_data))
        except Exception as e:
            logging.error(e)
            sys.exit(1)

async def asyncio_main(loop, workers_count):
    async with aiohttp.ClientSession(**get_client_session_kwargs()) as session:
        task_list = [redis_queue_worker(session)]+list(map(
            lambda i:request_worker(session),[None]*workers_count
        ))
        await asyncio.gather(*task_list, return_exceptions=True)


@click.command()
@click.argument('workers_count', required=True)
def main(workers_count):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(asyncio_main(loop, int(workers_count)))

if __name__ == '__main__':
    logging.debug("STARTED")
    main(prog_name='python -m aiohttp_rq')
