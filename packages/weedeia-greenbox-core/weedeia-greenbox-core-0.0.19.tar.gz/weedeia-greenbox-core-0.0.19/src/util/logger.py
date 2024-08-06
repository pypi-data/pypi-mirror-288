import logging

__log = logging.getLogger("CORE")

def configure(debug : bool = False) :
  if debug :
    logging.basicConfig(level=logging.DEBUG)
  else :
    logging.basicConfig(level=logging.ERROR)

def info(message : str) :
  __log.info(message)

def debug(message : str) :
  __log.debug(message)