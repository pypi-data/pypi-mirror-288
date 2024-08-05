import io
import json
import logging
import os
import sys
import uuid

import aiohttp


AIOHTTP_RQ_DIR = os.environ['AIOHTTP_RQ_DIR']
CONNECTOR_LIMIT = int(os.getenv("AIOHTTP_RQ_CONNECTOR_LIMIT", 100))
CONNECTOR_LIMIT_PER_HOST = int(os.getenv("AIOHTTP_RQ_CONNECTOR_LIMIT_PER_HOST", 0))
CHUNK_SIZE = int(os.getenv("AIOHTTP_RQ_CHUNK_SIZE", 100 * 1024))  # 100 KB Default
TTL_DNS_CACHE = int(os.getenv("AIOHTTP_RQ_TTL_DNS_CACHE", 10))  # 10 Default

def get_aiohttp_connector():
    # https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.TCPConnector
    return aiohttp.TCPConnector(
        limit=CONNECTOR_LIMIT,  # default 100
        limit_per_host=CONNECTOR_LIMIT_PER_HOST,  # default 0
        ttl_dns_cache=TTL_DNS_CACHE
        #enable_cleanup_closed=True,
    )

def get_aiohttp_timeout():
    # https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientTimeout
    return aiohttp.ClientTimeout(
        # total=60, # timeout for the whole request
        # connect=30, # timeout for acquiring a connection from pool
        #sock_connect=10,  # timeout for connecting to a peer for a new connection
        # sock_read=10,  # timeout for reading a portion of data from a peer
    )

def get_client_session_kwargs():
    return dict(
        connector=get_aiohttp_connector(),
        timeout=get_aiohttp_timeout()
    )

def get_content_path():
    return os.path.join(AIOHTTP_RQ_DIR,uuid.uuid4().hex)

async def write_content(response,content_path):
    f = io.BytesIO()
    try:
        while True:
            chunk = await response.content.read(CHUNK_SIZE)
            if not chunk:
                break
            f.write(chunk)
        content_dir = os.path.dirname(content_path)
        if not os.path.exists(content_dir):
            os.makedirs(content_dir)
        with open(str(content_path), "wb") as fd:
            fd.write(f.getbuffer())
    finally:
        f.close()
