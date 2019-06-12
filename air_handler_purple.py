
from datetime import datetime
import json
from urllib.request import urlopen

debug_no_GPIO = True

def switch_air_handler(air_handler_on):
    RELAY1 = 21
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY1, GPIO.OUT)

    if air_handler_on:
        GPIO.output(RELAY1, GPIO.HIGH)
    else:
        GPIO.output(RELAY1, GPIO.LOW)

aqi025_50 = 12.0
aqi100_50 = 54.0

pm025_limit = aqi025_50 / 5 # AQI < 10
pm100_limit = aqi100_50 / 5 # AQI < 10

pinside = json.load(urlopen('http://192.168.1.221/json?live=false'))
poutside = json.load(urlopen('http://192.168.1.208/json?live=false'))

pm025 = (pinside['p_2_5_um'] + pinside['p_2_5_um_b']) / 2
pm100 = (pinside['p_10_0_um'] + pinside['p_10_0_um_b']) / 2

if (pm025 > pm025_limit or pm100 > pm100_limit):
    air_handler_on = True
else:
    air_handler_on = False
air_handler_status = "ON" if air_handler_on else "OFF"

if not debug_no_GPIO:
    switch_air_handler(air_handler_on)

output_keys = ['p_1_0_um', 'p_1_0_um_b', 'p_2_5_um', 'p_2_5_um_b', 'p_10_0_um', 'p_10_0_um_b']
pinside['p_1_0_um_b'],pinside['p_1_0_um_b']
data = (datetime.now().isoformat(), air_handler_status,
    *[pinside[k] for k in output_keys], *[poutside[k] for k in output_keys])
print(",".join([str(d) for d in data]))
