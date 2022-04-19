import datetime

date = datetime.datetime.today()

yesterday = date - datetime.timedelta(1)  
date = yesterday.strftime('%Y_%m_%d')
# print(date)
print(date)