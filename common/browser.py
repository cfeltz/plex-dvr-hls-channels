from common.channel import Channel
from common.credentials import Credentials

class Browser:

    def __init__(self):
        self.credentials = None
        self.channels = None
    
    def load_config(self, config):
        self.credentials = Credentials(config['credentials'])

        channel_configs = config['channels']

        self.channels = []
        for channel_config in channel_configs:
            self.channels.append(Channel(channel_config))
    
    def channels_json(self):
        return [channel.__json__() for channel in self.channels]
