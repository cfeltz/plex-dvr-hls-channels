class Credentials:

    def __init__(self, config):
        self.__username = config['username']
        self.__password = config['password']
        self.__login_url = config['login_url']

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def login_url(self):
        return self.__login_url
