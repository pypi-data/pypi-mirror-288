__all__ = ['config']

from ._imports import *

config = configparser.ConfigParser()

if os.environ.get("CONFIG") == None:
    config.read(f'C:\\Users\\{getpass.getuser()}\\ds_config.txt')
else:
    config.read(os.environ.get("CONFIG"))

