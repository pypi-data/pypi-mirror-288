from argparse import Namespace
from ..service import gpio
import json

def validateConfig(args : Namespace):
    if len(args.pin) != len(args.mode) :
        raise Exception("Error: number of configs needs to be equal to number of pins")
    
def configure(args : Namespace) :
  gpio.setup(args.pin, args.mode)

def high(args):
   if args.pin:
      gpio.high(args.pin)

def low(args):
   if args.pin:
      gpio.low(args.pin)

def readBin(pin : list) :
   state = {}
   if pin:
      gpio.init()
      result = gpio.read(pin)
      state[f'p{pin}'] = result
      print(f'pin {pin} result: {result}')

   return json.dumps(state)