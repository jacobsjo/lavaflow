# Copied from https://discord.com/channels/900530660677156924/900545599106076703/1282509264069464134
# (slightly modified)

import logging
import time
from beet import Context
from beet.contrib.autosave import Autosave

import socket

logger = logging.getLogger("lively-reload")
startTime = 0


def beet_default(ctx: Context):
    autosave = ctx.inject(Autosave)

    global startTime
    startTime = time.time()

    autosave.add_link(finalize)


def finalize(ctx: Context):
    logger.info("Plugins took %s to complete", time.time() - startTime)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug("Connect to socket server")

    try:
        s.connect(("127.0.0.1", 25566))
    except:
        logger.debug("Failed to connect to socket server")
        return

    logger.debug("Connected to socket server, sending commands")

    commands = [
        '/tellraw @a ["", {{"text": "[Lively Reload] ", "bold": true, "color": "gray"}},{{"text": "Project has been built, time elapsed {time:.2f}s"}}]'.format(
            time=time.time() - startTime
        )
    ]
    s.send(bytes("\n".join(commands), "utf-8"))
    logger.debug("Done sending")
    s.close()
