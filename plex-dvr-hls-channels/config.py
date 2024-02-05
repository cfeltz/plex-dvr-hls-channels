import abc
import json


class Config:
    def __init__(self, config_path):
        self._config_path = config_path
        self._load()

    @abc.abstractmethod
    def _load(self):
        pass


class WriterConfig(Config):
    def __init__(self, config_path):
        self._channels_json_path = None
        super().__init__(config_path)

    def _load(self):
        with open(self._config_path, 'r') as config:
            config_json = json.load(config)
            self._channels_json_path = config_json['channels_json_path']

    @property
    def channels_json_path(self):
        return self._channels_json_path


class GrabberConfig(Config):
    def __init__(self, config_path):
        self._driver_path = None
        self._browser_config_path = None
        self._firefox_executable_path = None

        super().__init__(config_path)

    def _load(self):
        with open(self._config_path, 'r') as config:
            config_json = json.load(config)
            self._browser_config_path = config_json['web_config_path']

    @property
    def browser_config_path(self):
        return self._browser_config_path


class RequestServiceConfig(Config):

    def __init__(self, config_path):
        self._driver_path = None
        self._firefox_executable_path = None

        super().__init__(config_path)

    def _load(self):
        with open(self._config_path, 'r') as config:
            config_json = json.load(config)
            self._driver_path = config_json['driver_path']
            self._firefox_executable_path = config_json['firefox_executable_path']

    @property
    def driver_path(self):
        return self._driver_path

    @property
    def firefox_executable_path(self):
        return self._firefox_executable_path


class ReRouterConfig(Config):