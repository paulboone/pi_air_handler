import argparse

from air_handler_purple import switch_air_handler

parser = argparse.ArgumentParser(description='Turn on / off air handler. NOTE: does NOT change cron')
parser.add_argument('on', type=int, help='on=1, off=2')
args = parser.parse_args()

if args.on:
    print("Turning air handler on")
    switch_air_handler(True)
else:
    print("Turning air handler off")
    switch_air_handler(False)
