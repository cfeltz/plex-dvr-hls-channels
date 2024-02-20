from common.channel import Channel
from common.credentials import Credentials

class Browser:

    def __init__(self):
        self._credentials = None
        self._channels = None

    @property
    def credentials(self):
        return self._credentials

    @property
    def channels(self):
        return self._channels
    
    def create_channels(self, jsonObject):
        self._credentials = Credentials(jsonObject['credentials'])

        channel_configs = jsonObject['channels']

        self._channels = []
        for channel_config in channel_configs:
            self.channels.append(Channel(channel_config))
    
    def channels_json(self):
        return [channel.__json__() for channel in self.channels]
