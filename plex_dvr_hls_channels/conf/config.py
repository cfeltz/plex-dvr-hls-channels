from oslo_config import cfg

PLEX_GROUP = cfg.OptGroup(
    name='plex',
    title='Configuration for plex-dvr-hls-channels'
)

PLEX_OPTS = [
    cfg.StrOpt('driver_path',
               default=r'C:\Users\Chris\Desktop\geckodriver.exe',
               help='Path to your browser\'s driver.'),
    cfg.StrOpt('firefox_executable_path',
               default='C:\\Program Files\\Mozilla Firefox\\firefox.exe',
               help='Path to your browser executable.'),
    cfg.StrOpt('firefox_profile',
               help='Path to the firefox profile that has the passwords saved.',
               default=r'C:\Users\Chris\AppData\Roaming\Mozilla\Firefox\Profiles\pc6bgmmx.selenium'),
    cfg.StrOpt('channel_config',
               default='C:\\Users\\Chris\\repos\\plex-dvr-hls-channels\\etc\\channel-config.json'),
    cfg.StrOpt('plex_dvr_hls_channels_path',
               default=r'C:\Users\Chris\repos\plex-dvr-hls\channels.json',
               help='Path to the file that you will write the channel information to for plex-dvr-hls to read.'),
    cfg.StrOpt('m3u8s_directory',
               default=r'C:\Users\Chris\repos\plex-dvr-hls-channels\etc\m3u8s',
               help='Path to the folder where the latest m3u8s will be stored.'),
    cfg.StrOpt('log_file_path',
               default=r'C:\Users\Chris\repos\plex-dvr-hls-channels\etc\logs',
               help='Path to the folder where the latest m3u8s will be stored.'),
    cfg.StrOpt('localhost_port',
               default=8069,
               help='localhost port')
]


def register_opts(conf):
    conf.register_group(PLEX_GROUP)
    conf.register_opts(PLEX_OPTS, group=PLEX_GROUP)


def list_opts():
    return {
        PLEX_GROUP: PLEX_OPTS
    }
