from datetime import datetime
import pytz

def tm2daytime(timestamp):
    if len(str(timestamp)) == 13:
        dt_object = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%dT%H:%M:%S')
    else:
        dt_object = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S')
    return str(dt_object)

def utc2local(timestring):
    utc_time = datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%SZ")
    local_timezone = pytz.timezone('Europe/Athens')
    local_time=utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_time.strftime('%Y-%m-%dT%H:%M:%S')

timestring='2022-08-07T14:37:55Z'
print(utc2local(timestring))
# print(tm2daytime(1658683575820))
# print(datetime.now(timezone.utc).isoformat())

# your_date = parser.parse(th_tm)
# print(your_date)