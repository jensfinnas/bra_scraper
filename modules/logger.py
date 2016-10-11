# encoding: utf-8

import logging
import logging.config

ERROR_FORMAT = "%(levelname)s at %(asctime)s in %(funcName)s in %(filename) at line %(lineno)d: %(message)s"
DEBUG_FORMAT = "%(lineno)d in %(filename)s at %(asctime)s: %(message)s"
LOG_CONFIG = {
    'version':1,
    'formatters': {
        'error': { 'format':ERROR_FORMAT},
        'debug':{'format':DEBUG_FORMAT}
    },
    'handlers': {
        'console': {
            'class':'logging.StreamHandler',
            'formatter':'debug',
            'level':logging.DEBUG
            },
        'file': {
            'class':'logging.FileHandler',
            'filename':'scraper_errors.log',
            'formatter':'error',
            'level':logging.ERROR
        }
    },
    'root':{'handlers':('console', 'file'), 'level':'DEBUG'}
}
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)