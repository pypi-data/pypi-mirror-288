import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import logging
from schwab import Websocket
import orjson as json

def account_handler(message):
    for content in message['content']:
        message_type = content['2']
        message_content = ''
        if content['3']:
            message_content = json.loads(content['3'])
        print(message_type, message_content, sep='\t')


def handler(message):
    if 'data' in message:
        for item in message['data']:
            if item['service'] == 'ACCT_ACTIVITY':
                return account_handler(item)

logging.getLogger('schwab.websocket').setLevel(logging.DEBUG)

async def main():
    websocket = Websocket(provider='redis', host='192.168.1.154')
    subscriptions = (
        [websocket.subscribe_account],
        [websocket.subscribe_equities, ['AAPL', 'MSFT']],
    )
    await websocket.stream(subscriptions, handler)



asyncio.run(main())
