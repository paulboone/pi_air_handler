import urllib.request

def scrape(s, startstring, stopstring):
    idx = s.find(startstring)
    s1 = s[idx + len(startstring):]
    idx = s1.find(stopstring)
    return float(s1[0:idx]), s1

with urllib.request.urlopen('http://192.168.1.207/') as response:
    html = response.read().decode('utf-8')

pm025a, srem = scrape(html, "PM</font>2.5</b><br><b><font  style='font-size:140px'>", "</font>")
pm025b, srem = scrape(srem, "<font  style='font-size:140px'>", "</font>")
pm010a, srem = scrape(srem, "PM</font>10</b></td></tr><tr><td><b><font size=+4>", "</font>")
pm010b, srem = scrape(srem, "<font size=+4>", "</font>")
pm100a, srem = scrape(srem, "<font size=+4>", "</font>")
pm100b, srem = scrape(srem, "<font size=+4>", "</font>")

aqi025_50 = 12.0
aqi100_50 = 54.0

pm025_limit = aqi025_50 / 5 # AQI < 10
pm100_limit = aqi100_50 / 5 # AQI < 10

print(pm010a, pm010b, pm025a, pm025b, pm100a, pm100b)

if (pm025a > pm025_limit or pm100a > pm100_limit):
    print('air handler ON')
else:
    print('air handler OFF')
