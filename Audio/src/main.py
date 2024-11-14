import os
import sys

if not os.getcwd().endswith("app") or os.getcwd().endswith("Audio"):
    raise Exception("Script must be run from /Audio/ or /app/")
sys.path.append(os.getcwd())

import src.controllers.audio_to_sheet as ats

async def main(scope, receive, send):
    assert scope['type'] == 'http'

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })