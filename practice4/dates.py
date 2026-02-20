#Task 1
from datetime import datetime, timedelta


current_date = datetime.now()


new_date = current_date - timedelta(days=5)

print(new_date)

#Task 2

from datetime import date, timedelta

today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print(yesterday)
print(today)
print(tomorrow)

#Task 3

from datetime import datetime

now = datetime.now()

without = now.replace(microsecond=0)

print(without)

#Task 4

from datetime import datetime

date1_str = input()
date2_str = input()

date1 = datetime.strptime(date1_str, "%Y-%m-%d %H:%M:%S")
date2 = datetime.strptime(date2_str, "%Y-%m-%d %H:%M:%S")

difference = abs((date2 - date1).total_seconds())

print(int(difference))