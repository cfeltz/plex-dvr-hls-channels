import json

from common.browser import Browser
from common.service import RequestService

class Grabber:

    def __init__(self):
        self.__driver_path = None
        self.__channels_json_path = None
        self.__web_config_path = None
        self.__firefox_executable_path = None

        self._browsers = []

        self.__credentials = None
        self.__channels = None

    def load_config(self, config_path):
        with open(config_path, 'r') as config:
            config_json = json.load(config)

            self.__driver_path = config_json['driver_path']
            self.__channels_json_path = config_json['channels_json_path']
            self.__web_config_path = config_json['web_config_path']
            self.__firefox_executable_path = config_json['firefox_executable_path']

    def load_web_config(self):
        with open(self.__web_config_path, 'r') as web_config:
            configs = json.load(web_config)
            for config in configs:
                browser = Browser()
                browser.load_config(config)
                self._browsers.append(browser)

    def do_work(self):

        for browser in self._browsers:
            service = RequestService(self.__driver_path, self.__firefox_executable_path)

            service.login(browser.credentials)

            for channel in browser.channels:
                service.go_to_channel(channel)
            
            self.write_channels_json()

    def write_channels_json(self):
        with open(self.__channels_json_path, 'w') as channels_json_file:
            channel_json_list = []
            for browser in self._browsers:
                channel_json_list.extend(browser.channels_json())
            json.dump(channel_json_list, channels_json_file)

    def __str__(self):
        return f'{{'\
               f'\n\tself._driver_path: {self._driver_path}' \
               f'\n\tself._channels_json_path: {self._channels_json_path}' \
               f'\n\tself._channel_config_path: {self._channel_config_path}' \
               f'\n\tself._firefox_executable_path: {self._firefox_executable_path}' \
               f'\n}}'
