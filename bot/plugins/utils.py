import os
import shutil
from os import execl
from time import sleep
from sys import executable
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from bot import SUDO_USERS, DOWNLOAD_DIRECTORY, LOGGER
import psutil

@Client.on_message(filters.private & filters.incoming & filters.command(['log']) & filters.user(SUDO_USERS), group=2)
def _send_log(client, message):
  with open('log.txt', 'rb') as f:
    try:
      client.send_document(
        message.chat.id,
        document=f,
        file_name=f.name,
        reply_to_message_id=message.id
        )
      LOGGER.info(f'Log file sent to {message.from_user.id}')
    except FloodWait as e:
      sleep(e.x)
    except RPCError as e:
      message.reply_text(e, quote=True)

@Client.on_message(filters.private & filters.incoming & filters.command(['restart']) & filters.user(SUDO_USERS), group=2)
def _restart(client, message):
  shutil.rmtree(DOWNLOAD_DIRECTORY)
  LOGGER.info('Deleted DOWNLOAD_DIRECTORY successfully.')
  message.reply_text('**♻️Restarted Successfully !**', quote=True)
  LOGGER.info(f'{message.from_user.id}: Restarting...')
  execl(executable, executable, "-m", "bot")


def bytes_to_gb(bytes_value):
    return round(bytes_value / (1024 ** 3), 2)


@Client.on_message(filters.private & filters.incoming & filters.command(['stats']) & filters.user(SUDO_USERS), group=2)
def get_system_usage(client, message):
    # CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # RAM usage
    ram = psutil.virtual_memory()
    ram_usage = ram.percent
    ram_total_gb = bytes_to_gb(ram.total)
    ram_used_gb = bytes_to_gb(ram.used)
    ram_free_gb = bytes_to_gb(ram.available)

    # Storage usage
    disk = psutil.disk_usage('/')
    storage_usage = disk.percent
    storage_total_gb = bytes_to_gb(disk.total)
    storage_used_gb = bytes_to_gb(disk.used)
    storage_free_gb = bytes_to_gb(disk.free)

    msg = f"**System Stats**\n CPU Usage: {cpu_usage} % \n RAM Usage: {ram_usage} % ({ram_used_gb}/{ram_total_gb}) \n Storage Usage: {storage_usage}% ({storage_used_gb}/{storage_total_gb})\n"
    message.reply_text(msg, quote=True)