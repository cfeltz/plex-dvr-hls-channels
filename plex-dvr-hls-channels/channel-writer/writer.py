import json

class Writer:
    # writes channel json to file
    def __init__(self, config):
        # dict of channel id : channel
        self._channels = {}
        self._config = WriterConfig(config)

    def add_channels(self, channels: list):
        for channel in channels:
            self._channels[channel.id] = channel

    def write_channels_json(self):
        with open(self._channels_json_path, 'w') as channels_json_file:
            json.dump(list(self._channels.values()), channels_json_file)
