import fastapi.responses
import glob
import json
import logging
import os
import threading
import time

import plex_dvr_hls_channels.conf


from plex_dvr_hls_channels import web

from fastapi import FastAPI


CONF = plex_dvr_hls_channels.conf.CONF
app = FastAPI()
logger = logging.getLogger(__name__)
# logging.basicConfig(filename=os.path.join(CONF.plex.log_file_path, 'logs.txt'), level=logging.INFO)
logging.basicConfig(level=logging.INFO)

CHANNEL_CONFIGS = web.CHANNEL_CONFIGS
ACTIVE_THREAD_LOCK = threading.RLock()


def log_setup():
    os.makedirs(f'{CONF.plex.log_file_path}', exist_ok=True)
    logging.basicConfig(filename=os.path.join(CONF.plex.log_file_path, 'logs.txt'), level=logging.INFO)
    open(os.path.join(CONF.plex.log_file_path, 'logs.txt'), 'w').close()
    seleniumwire_logging = logging.getLogger('seleniumwire')
    seleniumwire_logging.setLevel(logging.ERROR)


def create_channels():
    global CHANNEL_CONFIGS

    list_of_channel_jsons = []

    with open(CONF.plex.channel_config) as channel_configs_json:
        channel_configs = json.load(channel_configs_json)
        for channel_config in channel_configs:
            list_of_channel_jsons.append(channel_json(channel_config))

            CHANNEL_CONFIGS[int(channel_config['number'])] = channel_config
            os.makedirs(f'{CONF.plex.m3u8s_directory}\\{channel_config["number"]}', exist_ok=True)

    with open(CONF.plex.plex_dvr_hls_channels_path, 'w') as channels_json_file:
        json.dump(list_of_channel_jsons, channels_json_file)


def channel_json(channel_config):
    return {
        'name': channel_config['name'],
        'url': f'http://localhost:{CONF.plex.localhost_port}/channel/{channel_config["number"]}',
        'id': int(channel_config['number']),
    }


async def _get_most_recent_m3u8_file(channel_number):
    files = None
    while not files:
        files = glob.glob(os.path.join(CONF.plex.m3u8s_directory, str(channel_number), '*'))

    most_recent_file = max(files, key=os.path.getmtime)
    return most_recent_file


async def _get_thread_for_channel_number(number):
    threads = threading.enumerate()
    if not threads:
        logger.info('threading is none')

    for thread in threads:
        if isinstance(thread, web.ChannelThread) and int(thread.number) == int(number):
            return thread

    logger.info(f'get_channel_number: {number} thread starting')
    new_thread = web.ChannelThread(CHANNEL_CONFIGS[number])
    new_thread.start()
    logger.info(f'get_channel_number: {number} thread started')

    return new_thread


def _remove_old_files(file_age_expiration_threshold=3600):
    global CHANNEL_CONFIGS
    current_time = time.time()
    for channel_config in CHANNEL_CONFIGS.values():
        directory_contents = os.listdir(os.path.join(CONF.plex.m3u8s_directory, str(channel_config['number'])))

        for directory_object in directory_contents:
            path = os.path.join(CONF.plex.m3u8s_directory, str(channel_config['number']), directory_object)

            if os.path.isfile(path):
                file_age = current_time - os.path.getmtime(path)
                if file_age > file_age_expiration_threshold:
                    logger.info(f'Removing {path}')
                    os.remove(path)


def cleanup(cleanup_interval=30):
    while True:
        _remove_old_files()
        time.sleep(cleanup_interval)


@app.get('/channel/{number}')
async def get_channel_number(number: int):
    logger.info(f'get_channel_number: {number}')
    global CHANNEL_CONFIGS

    thread_for_number = await _get_thread_for_channel_number(number)

    thread_for_number.file_has_been_written.wait()

    file = await _get_most_recent_m3u8_file(number)
    logger.info(f'get_channel_number: {number} returning path {file}')
    return fastapi.responses.FileResponse(file, filename=os.path.basename(file))
