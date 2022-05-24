import asyncio
import os
import subprocess
import time

import psutil
from pyrogram import filters
from pyrogram.errors import FloodWait

from EmikoRobot import (
    BOT_ID,
    app,
    bot_start_time,
)


async def bot_sys_stats():
    bot_uptime = int(time.time() - bot_start_time)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    stats = f"""
@KoboKanaeru_Robot
------------------
PlatForm : Linux
PlatForm - Release : 4.4.0-1101-aws
PlatFork - Version : #106-Ubuntu SMP Tue Mar 1 10:51:49 UTC 2022
Architecture : x86_64
Hostname : aa5a53a6-d922-4d19-9c0e-dca30cb2e74d
IP : 172.17.216.82
Mac : 0a:89:7d:e1:ac:b3

BOT: {round(process.memory_info()[0] / 1024 ** 2)} MB
CPU: {cpu}%
RAM: {mem}%
DISK: {disk}%

UPTIME: {formatter.get_readable_time(bot_uptime)}
"""
    return stats
