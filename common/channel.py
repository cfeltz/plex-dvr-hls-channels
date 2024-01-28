class Channel:

    def __init__(self, config):
        self._name = config['name']
        self._id = int(config['id'])
        self._web_url = config['web_url']
        self._stream_url = ''

    def get_name(self):
        return self._name
    
    @property
    def web_url(self):
        return self._web_url

    @property
    def stream_url(self):
        return self._stream_url

    @stream_url.setter
    def stream_url(self, stream_url):
        if isinstance(stream_url, str):
            self._stream_url = stream_url
        else:
            raise Exception('Not cool bro, trynna set the stream_url to not a string?')

    def __json__(self):
        return { 
                'name': self._name,
                'url':  self._stream_url,
                'id':   int(self._id)
            }
