from rift import conf as settings
from rift.utils.log import configure_logging


def setup():
    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
