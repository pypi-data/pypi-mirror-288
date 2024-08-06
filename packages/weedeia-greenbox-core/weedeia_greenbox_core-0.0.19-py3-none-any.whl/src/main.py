from argparse import ArgumentParser, Namespace
from .constants import operations, pinmode
from .util import logger
import .action

def execute (args: Namespace):
  result = {}
  if args.action == operations.configure :
    action.validateConfig(args)
    action.configure(args)
  elif args.action == operations.high :
    action.high(args)
  elif args.action == operations.low :
    action.low(args)
  elif args.action == operations.readBin:
    result = action.readBin(args)

  print(result)
    

parser = ArgumentParser(
  prog="weedeia-greenbox-core",
  description="Respberry GPIO configuration and controller")

parser.add_argument(
  "-v", 
  "--verbose", 
  dest="verbose",
  type=bool,
  help="pring dev logs",
  default=False,
  choices = [ True, False ] )
parser.add_argument(
  "-a", 
  "--action", 
  dest="action",
  type=str,
  help="what action you want to execute",
  choices = [
    operations.configure,
    operations.high,
    operations.low,
    operations.readBin
  ])
parser.add_argument(
  "-p", 
  "--pin", 
  dest="pin", 
  type=int,
  nargs="+",
  help="configure gpio pins",
  choices=[12, 23, 17 , 27, 24, 25, 4, 26, 16, 20, 21, 19, 22, 5, 6, 13])
parser.add_argument(
  "-m", 
  "--mode", 
  dest="mode", 
  type=str,
  nargs="+",
  help="pin mode",
  choices=[pinmode.IN, pinmode.OUT, pinmode.INUP])

args = parser.parse_args()

logger.configure(args.verbose)
if args.verbose:
  logger.debug(f'Action: {args.action}')
  logger.debug(f'Pins: {args.pin}')
  logger.debug(f'Modes: {args.mode}')

execute(args)