import wled_light as wled 
import time
import json 
import requests
import sys 
import os
import logging
from datetime import datetime, timedelta

# Set up logging at info level
logging.basicConfig(filename='stoplight.log', level=logging.INFO) 

#Open the config file
with open('wled_config.json') as f:
    config = json.load(f)

#create a new instance of the WLED class
stoplight = wled.Wled_Strip(config['server_ip'], config['start_time'], config['end_time'])

def get_current_time():
    #Get the current time from the system without the date and microseconds
    current_time = datetime.now().time().replace(microsecond=0)
    return current_time

#From the stoplight object, get the start and end times
start_time = stoplight.start_time
end_time = stoplight.end_time

#convert the start and end times to datetime objects
start_time = datetime.strptime(start_time, '%H:%M:%S').time()
end_time = datetime.strptime(end_time, '%H:%M:%S').time()

#This while loop checks to see if the current time is less than the start time. If it is, it will sleep for 5 seconds and check again
while True:
    cur_time = get_current_time()

    if cur_time < start_time:
        print(f'Current time is {cur_time}. Waiting for {start_time}')
        time.sleep(5)
    else:
        break

#This while loop checks the values of the minute and seconds of the current time.
#If the minute integer equals certain values, it will perform actions on the stoplight object
cur_time = get_current_time()

while start_time <= cur_time <= end_time:
    cur_time = get_current_time()
    
    print(f'Current time is {get_current_time()}')

    if cur_time.minute == 0:
        stoplight.redlight()
        print("Red Light called")
        logging.info(f"Red Light called at {get_current_time()}")
        #calculate the number of seconds until minute 1 and zero seconds and sleep for that amount of time
        sleep_time = 60 - get_current_time().second
        print(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)
    
    elif 1 <= cur_time.minute <= 58:
        stoplight.greenlight()
        print(f"Green Light called at {get_current_time()}")
        logging.info(f"Green Light called at {get_current_time()}")
        #calculate the number of seconds until the 59th minute of the hour and sleep for that amount of time
        sleep_time = 3540 - (get_current_time().minute * 60 + cur_time.second)
        print(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)
        
    
    elif cur_time.minute == 59:
        stoplight.yellowlight()
        print(f"Yellow Light called at {get_current_time()}")
        logging.info(f"Yellow Light called at {get_current_time()}")
        #calculate the number of seconds until the next hour and sleep for that amount of time
        sleep_time = 60 - get_current_time().second
        print(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)
        
    
    cur_time = get_current_time()


#turn off the lights
stoplight.shutdown()
logging.info("Stoplight control script stopped at " + time.strftime('%H:%M:%S'))
print("Stoplight control script stopped at " + time.strftime('%H:%M:%S'))