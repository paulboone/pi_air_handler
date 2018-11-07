from datetime import datetime
import urllib.request

debug_no_GPIO = False

def switch_air_handler(air_handler_on):
    RELAY1 = 21
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY1, GPIO.OUT)

    if air_handler_on:
        GPIO.output(RELAY1, GPIO.HIGH)
    else:
        GPIO.output(RELAY1, GPIO.LOW)



def scrape(s, startstring, stopstring):
    idx = s.find(startstring)
    s1 = s[idx + len(startstring):]
    idx = s1.find(stopstring)
    return float(s1[0:idx]), s1

def get_purple_air_pms(url):
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')

    pm025a, srem = scrape(html, "PM</font>2.5</b><br><b><font  style='font-size:140px'>", "</font>")
    pm025b, srem = scrape(srem, "<font  style='font-size:140px'>", "</font>")
    pm010a, srem = scrape(srem, "PM</font>10</b></td></tr><tr><td><b><font size=+4>", "</font>")
    pm010b, srem = scrape(srem, "<font size=+4>", "</font>")
    pm100a, srem = scrape(srem, "<font size=+4>", "</font>")
    pm100b, srem = scrape(srem, "<font size=+4>", "</font>")

    return [pm010a, pm010b, pm025a, pm025b, pm100a, pm100b]

pinside = get_purple_air_pms('http://192.168.1.207/')
poutside = get_purple_air_pms('http://192.168.1.208/')

aqi025_50 = 12.0
aqi100_50 = 54.0

pm025_limit = aqi025_50 / 5 # AQI < 10
pm100_limit = aqi100_50 / 5 # AQI < 10

if (pinside[2] > pm025_limit or pinside[4] > pm100_limit):
    air_handler_on = True
else:
    air_handler_on = False
air_handler_status = "ON" if air_handler_on else "OFF"

if not debug_no_GPIO:
    switch_air_handler(air_handler_on)

data = (datetime.now().isoformat(), air_handler_status, *pinside, *poutside)
print(",".join([str(d) for d in data]))
