from os.path import realpath, join, dirname
import logging

log_file = realpath(join(dirname(__file__),"connect4.log"))
logging.basicConfig(filename=log_file, filemode="w+", level=logging.DEBUG)
log = logging.getLogger(__name__)
