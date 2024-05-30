import logging
import uvicorn
import threading

from plex_dvr_hls_channels import utils

import plex_dvr_hls_channels.conf

CONF = plex_dvr_hls_channels.conf.CONF
app = utils.app
logger = logging.getLogger(__name__)


def main():
    CONF(default_config_files=['config.conf'])

    utils.log_setup()
    utils.create_channels()
    cleanup_thread = threading.Thread(target=utils.cleanup)
    cleanup_thread.start()

    uvicorn.run(app, host='127.0.0.1', port=CONF.plex.localhost_port)


if __name__ == '__main__':
    main()
