import time

import zmq
from zmq.asyncio import Context, Poller
import asyncio

import huep


async def sender(blocka, blockb, blockc, blockd):

    ctx = Context.instance()
    print("<PUSHING SERVER...>")
    url = 'tcp://127.0.0.1:5555'
    tic = time.time()
    push = ctx.socket(zmq.PUSH)
    push.bind(url)

    combined = str(blocka)+"x"+str(blockb)+"x"+str(blockc)+"x"+str(blockd)
    await push.send_multipart([str(combined).encode('ascii')])
    await asyncio.sleep(0.1)

def handler(blocka, blockb, blockc, blockd):
    asyncio.run(sender(blocka, blockb, blockc, blockd))
