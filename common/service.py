import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.service import Service

from common.channel import Channel


class RequestService:


    def __init__(self, driver_path, firefox_executable_path=None):
        service = Service(executable_path=driver_path)
        options = webdriver.FirefoxOptions()
        if firefox_executable_path:
            options.binary_location = firefox_executable_path
        self.__driver = webdriver.Firefox(service=service, options=options)

    def login(self, credential):
        self.__driver.get(credential.login_url)

        self.__driver.implicitly_wait(5)

        username_input = self.__driver.find_element(By.ID, 'username')
        username_input.send_keys(credential.username)

        password_input = self.__driver.find_element(By.ID, 'password')
        password_input.send_keys(credential.password)

        password_input.send_keys(Keys.RETURN)

        # let the login flow finish
        time.sleep(5)


    def go_to_channels(self, channels):
        for channel in channels:
             self.go_to_channel(channel)

    def go_to_channel(self, channel):
        self.__driver.get(channel.web_url)

        # let the network logs build up
        time.sleep(8)

        # dump the logs
        network_requests = self.__driver.execute_script(
                "var performance = window.performance || " \
                "window.mozPerformance || " \
                "window.msPerformance || " \
                "window.webkitPerformance || " \
                "{}; var network = performance.getEntries() ||" \
                "{}; return network;"
                )

        # filter the urls for the m3u8 links that we care about
        network_requests = filter_requests(network_requests)

        shortest_url = network_requests[0]
        for request in network_requests[1:]:
            if len(request['name']) < len(shortest_url['name']):
                shortest_url = request

        channel.stream_url = shortest_url['name']

        # return the modified channel
        return channel

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

