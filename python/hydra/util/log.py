'''
    logger module for spider
'''
import sys, logging

Logger = logging.getLogger("spider")

Logger.addHandler(logging.StreamHandler(sys.stdout))

Logger.setLevel(logging.INFO)

