import pytz

f = open("pytz_timezones_list.txt", "w+")
f.write("\n".join(pytz.all_timezones))
f.close()
