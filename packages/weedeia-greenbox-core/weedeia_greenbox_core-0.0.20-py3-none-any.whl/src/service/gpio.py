try:
    import RPi.GPIO as GPIO
except (Exception):
    from .MockGPIO import GPIO
from ..util import logger
from ..constants import pinmode

def init():
   GPIO.setmode(GPIO.BCM)

def _setPinHighOrLow(pins : list, high : bool):
  init()
  for pin in enumerate(pins):
    state = GPIO.HIGH if high else GPIO.LOW
    logger.debug(f'Change pin {pin} to {state}')
    GPIO.output(pin, state)

def _parseMode(mode: str):
   if mode == pinmode.IN:
      return GPIO.IN
   elif mode == pinmode.OUT:
      return GPIO.OUT
   elif mode == pinmode.INUP:
    return pinmode.INUP
   else:
      raise Exception(f'Invalid pin mode: {mode}')

def setup(pins : list, mode : list):
  init()
  for idx, pin in enumerate(pins):
    pmode = _parseMode(mode[idx])
    logger.debug(f'Setting pin {pin} to mode {pmode}')
    if pmode == pinmode.INUP:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    else:
      GPIO.setup(pin, pmode)

def high(pins : list):
  _setPinHighOrLow(pins, True)

def low(pins : list):
  _setPinHighOrLow(pins, False)

def read(pin: int):
  return GPIO.input(pin)
#def set_ReadyLight(active : str) :
   #set_pin_output_high(READY_LIGHT, _is_on(active))