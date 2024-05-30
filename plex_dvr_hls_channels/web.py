import brotli
import gzip
import logging
import os
import random
import re
import string
import threading
import time

import plex_dvr_hls_channels.conf

from plex_dvr_hls_channels import session

CONF = plex_dvr_hls_channels.conf.CONF
CHANNEL_CONFIGS = {}
logger = logging.getLogger(__name__)
# logging.basicConfig(filename=os.path.join(CONF.plex.log_file_path, 'logs.txt'), level=logging.INFO)
logging.basicConfig(level=logging.INFO)


class ChannelThread(threading.Thread):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = config['name']
        self.number = int(config['number'])
        try:
            self.regex = re.compile(config['regex'])
        except KeyError as e:
            self.regex = re.compile(r'.m3u8')

        self.url = config['url']
        self.browser = session.Firefox()

        self.previous_download_url = None

        self.expired = threading.Event()
        self.file_has_been_written = threading.Event()

    def run(self):
        logger.info(f'{self.number}: start_driver')
        self.browser.start_driver(self.url)

        logger.info(f'{self.number}: entering while loop')
        while not self.expired.is_set():
            download_url = self.browser.get_most_recent_m3u8_request(self.regex)
            if download_url == self.previous_download_url:
                logger.info(f'{self.number}: skipping repeat download_url')
                continue
            logger.info(f'{self.number}: request {download_url}')
            self.previous_download_url = download_url
            self.download_file(download_url)

        self.browser.stop_driver()

    def download_file(self, request):
        filename = self.generate_file_name('guh.m3u8')
        filepath = os.path.join(CONF.plex.m3u8s_directory, str(self.number), filename)
        m3u8_bytes = self.decompress_content(request.response.body, request.response.headers['Content-Encoding'])
        m3u8_content = m3u8_bytes.decode('utf-8')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(m3u8_content)
            self.file_has_been_written.set()

    @staticmethod
    def generate_file_name(original_file_name, length=30):
        original_file_name = original_file_name.split('.')

        characters = string.ascii_letters + string.digits

        random_string = ''.join(random.choice(characters) for _ in range(length))

        original_file_name[0] = str(random_string)
        return '.'.join(original_file_name)

    @staticmethod
    def decompress_content(content, encoding):
        if encoding == 'gzip':
            return gzip.decompress(content)
        elif encoding == 'br':
            return brotli.decompress(content)
        return content
