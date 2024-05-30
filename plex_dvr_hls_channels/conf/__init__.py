from oslo_config import cfg

from plex_dvr_hls_channels.conf import config as plex

CONF = cfg.CONF

plex.register_opts(CONF)
