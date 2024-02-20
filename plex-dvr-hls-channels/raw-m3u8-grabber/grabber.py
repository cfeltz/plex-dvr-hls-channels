import json

from common.browser import Browser
from common.service import RequestService

class Grabber:

    def __init__(self, config):
        self._browsers = []
        self._credentials = None
        self._channels = None

        self._config = GrabberConfig(config)

    def create_browsers(self):
        with open(self._config.browser_config_path, 'r') as web_config:
            configs = json.load(web_config)
            for config in configs:
                browser = Browser()
                browser.create_channels(config)
                self._browsers.append(browser)

    def do_work(self):
        for browser in self._browsers:
            service = RequestService(self._config.driver_path, self._config.firefox_executable_path)
            if browser.credentials:
                service.login(browser.credentials)

            service.get_stream_urls(browser.channels)

    def get_channels_json(self):
        channel_json_list = []
        for browser in self._browsers:
            channel_json_list.extend(browser.channels_json())
        return channel_json_list
