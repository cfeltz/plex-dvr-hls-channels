import unittest

from plex_dvr_hls_channels import web

import plex_dvr_hls_channels.conf

CONF = plex_dvr_hls_channels.conf.CONF


class WebTest(unittest.TestCase):
    def setUp(self):
        CONF(default_config_files=['C:\\Users\Chris\\repos\\plex-dvr-hls-channels\\config.conf'])

    def test_create_channels(self):
        web.create_channels()


    def test_write_channels(self):
        web.create_channels()
        web.write_channels_json()