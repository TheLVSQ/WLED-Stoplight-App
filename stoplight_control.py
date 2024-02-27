import wled_light as wled 
import time
import json 
import requests
import sys 
import os
import logging
from datetime import datetime, timedelta
from time import ctime

# Define the next change time based on current time
def next_change_time(current_time):
    # Calculate next minute for changes between green, yellow, and red
    if current_time.minute < 59:
        # If current minute is less than 59, next change is the next minute
        next_change = current_time + timedelta(minutes=1)
        next_change = next_change.replace(second=0)  # Reset seconds to 0 for the start of the minute
    else:
        # If current minute is 59, next change is at the top of the next hour
        next_change = (current_time + timedelta(hours=1)).replace(minute=0, second=0)
    return next_change

#get the current time
cur_time = datetime.now()


#log the time and date of start up
logging.basicConfig(filename='stoplight.log', level=logging.INFO) 
logging.info(f"Time: {cur_time.strftime('%H:%M:%S')}, Date: {time.strftime('%m/%d/%Y')}")
logging.info("Stoplight control script started")

#open the config json file
with open('wled_config.json') as json_file:
    config = json.load(json_file)

#create a new instance of the WLED class
stoplight = wled.Wled_Strip(config['server_ip'], config['start_time'], config['end_time'])

#This script needs to run in a loop during the start and end times from the config file. 
#They are stored as strings in "HH:MM:SS" format, so we need to convert them to datetime objects
start_time = datetime.strptime(config['start_time'], '%H:%M:%S')
end_time = datetime.strptime(config['end_time'], '%H:%M:%S')

#If execution begins before the start time, wait until the start time
while True:
    #update the current time
    current_time = datetime.now()

    #compare the current time to the start time
    if current_time < start_time:
        print(f"Waiting for start time: {start_time}")
        time.sleep(5)
    else:
        break
    

#run the loop while the current time is between the start and end times
while current_time >= start_time and current_time <= end_time:
    #update the current time
    current_time = datetime.now()
    next_change = next_change_time(current_time)
    
    print(f"Next change: {next_change}")
    
    current_hour = current_time.hour
    current_minute = current_time.minute
    current_second = current_time.second

    print(current_time)
    logging.info(f"Time: {current_time}")
    
    #if the minute and second of the current time is between XX:01:00 and XX:01:59, turn on the green light
    
    if 1 <= current_minute <= 58:
        stoplight.greenlight()
        print("Green light on")
        
    elif current_minute == 59:
        stoplight.yellowlight()
        print("Yellow light on")

    elif current_minute == 0:
        stoplight.redlight()
        print("Red light on")
        
    # Calculate sleep duration as the difference between now and the next change time
    sleep_duration = (next_change - datetime.now()).total_seconds()
    print(f"Sleeping for {sleep_duration} seconds until the next change.")
    time.sleep(sleep_duration)

#turn off the lights
stoplight.shutdown()
logging.info("Stoplight control script stopped at " + time.strftime('%H:%M:%S'))

