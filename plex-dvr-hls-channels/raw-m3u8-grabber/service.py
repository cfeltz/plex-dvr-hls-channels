import time
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.service import Service


class RequestService:

    def __init__(self, config_path):
        self._config = RequestServiceConfig(config_path)
        self._driver = None
        self._initiate_driver()

    def _initiate_driver(self):
        service = Service(executable_path=self._config.driver_path)
        options = webdriver.FirefoxOptions()
        if self._config.firefox_executable_path:
            options.binary_location = self._config.firefox_executable_path
        self._driver = webdriver.Firefox(service=service, options=options)

    def login(self, credential):
        self._driver.get(credential.login_url)

        self._driver.implicitly_wait(5)

        username_input = self._driver.find_element(By.ID, 'username')
        username_input.send_keys(credential.username)

        password_input = self._driver.find_element(By.ID, 'password')
        password_input.send_keys(credential.password)

        password_input.send_keys(Keys.RETURN)

        # let the login flow finish
        time.sleep(5)

    def go_to_channels(self, channels):
        for channel in channels:
            self.go_to_url(channel)
            if not channel.stream_url():
                channel.stream_url = self._get_shortest_network_request(channel.regex)
                continue

    def go_to_url(self, channel):
        self._driver.get(channel.web_url)

    def get_shortest_network_request(self, regex, wait_for_network_logs=8):
        time.sleep(wait_for_network_logs)
        # dump the logs
        network_requests = self._driver.execute_script(
            "var performance = window.performance || "
            "window.mozPerformance || "
            "window.msPerformance || "
            "window.webkitPerformance || "
            "{}; var network = performance.getEntries() ||"
            "{}; return network;"
        )

        # filter the urls for the links that we care about
        network_requests = filter_requests(regex, network_requests)

        shortest_url = network_requests[0]
        for request in network_requests[1:]:
            if len(request['name']) < len(shortest_url['name']):
                shortest_url = request

        return shortest_url['name']


class StreamEastService(Service):

    def __init__(self):
        super().__init__()


def filter_requests(regex, requests):
    filtered = []

    for request in requests:
        if request['name'] and re.match(regex, request['name']):
            filtered.append(request)
    
    return filtered

