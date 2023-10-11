import logging
logger = logging.getLogger("DeepStacker")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("DeepStacker.log")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)