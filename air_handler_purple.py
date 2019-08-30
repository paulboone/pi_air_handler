
from datetime import datetime
import json
from urllib.request import urlopen

from air_handler.utils import switch_air_handler, load_config, load_runstate

config = load_config()
state = load_runstate()

# define particle limits to hit a threshold AQI of 50 for 025 and 100 particle sizes
aqi025_50 = 12.0
aqi100_50 = 54.0

# define particle limits based on configured aqi theshold
pm025_limit = aqi025_50 * config['aqi_threshold']/ 50
pm100_limit = aqi100_50 * config['aqi_threshold']/ 50

# load Purple Air data
pinside = json.loads(urlopen(config['pa_indoor_endpoint']).read().decode('utf-8'))
poutside = json.loads(urlopen(config['pa_outdoor_endpoint']).read().decode('utf-8'))

# average both sensors to get actual particulate readings
pm025 = (pinside['pm2_5_atm'] + pinside['pm2_5_atm_b']) / 2
pm100 = (pinside['pm10_0_atm'] + pinside['pm10_0_atm_b']) / 2

# turn air handler on if particulate limits are exceeded
air_handler_on = (pm025 > pm025_limit or pm100 > pm100_limit)
if not config['debug_no_GPIO'] and state==2:
    switch_air_handler(air_handler_on, config['relay_num'])

if state == 2:
    air_handler_status = "AUTO-ON" if air_handler_on else "AUTO-OFF"
elif state == 1:
    air_handler_status = "ON"
    air_handler_statue += "/ON" if air_handler_on else "/OFF"
elif state == 0:
    air_handler_status = "OFF"
    air_handler_statue += "/ON" if air_handler_on else "/OFF"

output_keys = ['pm1_0_atm', 'pm1_0_atm_b', 'pm2_5_atm', 'pm2_5_atm_b', 'pm10_0_atm', 'pm10_0_atm_b']

data = (datetime.now().isoformat(), air_handler_status,
    *[pinside[k] for k in output_keys], *[poutside[k] for k in output_keys])

print(",".join([str(d) for d in data]))
