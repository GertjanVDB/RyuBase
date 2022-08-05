import logging
from logging import getLogger, basicConfig, DEBUG, INFO
basicConfig(level=DEBUG)
logger = getLogger()

logger.info('App started')

# imports
import db


logger.info('App Finished')