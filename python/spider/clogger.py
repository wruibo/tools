'''
    logger module for spider
'''
import sys, logging

logger = logging.getLogger("spider")

logger.addHandler(logging.StreamHandler(sys.stdout))

logger.setLevel(logging.INFO)
