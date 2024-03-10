from seleniumwire import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

import plex_dvr_hls_channels.conf

CONF = plex_dvr_hls_channels.conf.CONF


class Firefox:
    def __init__(self):
        self._driver = None

    def start_driver(self, url):
        if self._driver:
            return None
        service = Service(executable_path=CONF.plex.driver_path)
        options = Options()
        options.binary_location = CONF.plex.firefox_executable_path
        options.profile = CONF.plex.firefox_profile
        # options.headless = True
        # headless only worked after I manually added this argument, I'm leaving both since it works
        options.add_argument('--headless')
        options.set_preference('permissions.default.image', 2)
        options.set_preference('toolkit.cosmeticAnimations.enabled', False)
        options.set_preference('dom.ipc.processCount', 1)

        self._driver = webdriver.Firefox(service=service, options=options)
        self._driver.get(url)

    def stop_driver(self):
        self._driver.quit()

    def get_most_recent_m3u8_request(self, regex, wait_for_network_logs=8):
        self._driver.implicitly_wait(wait_for_network_logs)
        filtered_requests = []

        while not filtered_requests:
            for request in self._driver.requests:
                if (request.url and regex.search(request.url) and request.response and request.response.headers and
                        'application/vnd.apple.mpegurl' in
                        request.response.headers['Content-Type']):
                    filtered_requests.append(request)

        sorted_filtered_requests = sorted(
            filtered_requests,
            key=lambda x: (x.date, x.url),
            reverse=True
        )

        return sorted_filtered_requests[0]
