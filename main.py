from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.service import Service


import time
import json

login_url = 'https://watch.freecast.com/login/?next=/channels/'
credentials_path = 'credentials.txt'
driver_path = 'geckodriver'
firefox_executable_path = None
channels_json_path = 'channels.json'

channel_config_path = 'channel-config.json' 

channel_objects = []

def main():
   
    create_channels(channel_config_path)

    selenium_magic()

    write_channels_json()

    return "fortnite"

def create_channels(channel_config_path):

    with open(channel_config_path, 'r') as channel_config:
        channel_list = json.load(channel_config)
        for channel in channel_list:
            channel_objects.append(Channel(channel))


def selenium_magic():

    service = Service(executable_path=driver_path)
    options = webdriver.FirefoxOptions()
    if firefox_executable_path:
        options.binary_location = firefox_executable_path
    driver = webdriver.Firefox(service=service, options=options)

    login = read_credentials(credentials_path)

    try:
        driver.get(login_url)

        driver.implicitly_wait(5)

        username_input = driver.find_element(By.ID, 'username')
        username_input.send_keys(login['username'])

        password_input = driver.find_element(By.ID, 'password')
        password_input.send_keys(login['password'])

        password_input.send_keys(Keys.RETURN)

        # let the login flow finish
        time.sleep(5)

        for channel in channel_objects:
            driver.get(channel.get_web_url())

            # let the network logs build up
            time.sleep(8)

            # dump the logs
            network_requests = driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")

            # filter the urls for the m3u8 links that we care about
            network_requests = filter_requests(network_requests)

            shortest_url = network_requests[0]
            for request in network_requests[1:]:
                if len(request['name']) < len(shortest_url['name']):
                    shortest_url = request

            channel.set_stream_url(shortest_url['name'])

    except Exception as ex:
        print(ex)


def filter_requests(requests):
    print('Starting filtering')
    filtered = []

    for request in requests:
        if 'name' in request.keys():
            if '.m3u8' in request['name']: 
                filtered.append(request)
    
    print('Finished filtering')
    print(f'filtered: {filtered}')
    return filtered



def read_credentials(file_name):
    login = {}
    with open(file_name, 'r') as file:
        login['username'] = file.readline().strip()
        login['password'] = file.readline().strip()

    return login


class Channel:

    def __init__(self, unwrapped_json):
        self._name = unwrapped_json['name']
        self._id = unwrapped_json['id']
        self._web_url = unwrapped_json['web_url']
        self._stream_url = ''

    def get_name(self):
        return self._name

    def get_web_url(self):
        return self._web_url

    def get_stream_url(self):
        return self._stream_url

    def set_stream_url(self, stream_url):
        self._stream_url = stream_url

    def __json__(self):
        return { 
                'name': self._name,
                'url':  self._stream_url,
                'id':   self._id
            }


def write_channels_json():
    with open(channels_json_path, 'w') as channels_json_file:
        channel_json_list = []
        for channel in channel_objects:
            channel_json_list.append(channel.__json__())
        json.dump(channel_json_list, channels_json_file)

if __name__ == '__main__':
    main()
