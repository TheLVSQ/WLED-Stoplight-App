import wled_light as wled 
import time
import json 
import requests
import sys 
import os
import logging
from datetime import datetime

#create a function that will accept a number of seconds and every 10 seconds output to the console
#the remaining number of seconds. Use the \b character to overwrite the previous line
def countdown(seconds):
    start_time = time.time()
    remaining = seconds
    while remaining > 0:
        sys.stdout.write(f'{remaining} seconds remaining...')
        sys.stdout.flush()  # Ensure the output is updated immediately
        time.sleep(10)  # Wait for 10 seconds
        elapsed = time.time() - start_time
        remaining = seconds - int(elapsed)
    sys.stdout.write('\rDone!\n')  # Overwrite the last line with "Done!"

#log the time and date of start up
logging.basicConfig(filename='stoplight.log', level=logging.INFO) 
logging.info(f"Time: {time.strftime('%H:%M:%S')}, Date: {time.strftime('%m/%d/%Y')}")
logging.info("Stoplight control script started")

#open the config json file
with open('wled_config.json') as json_file:
    config = json.load(json_file)

#create a new instance of the WLED class
stoplight = wled.Wled_Strip(config['server_ip'], config['start_time'], config['end_time'])

#This script needs to run in a loop during the start and end times from the config file:
start_time = config['start_time']
end_time = config['end_time']

#If execution begins before the start time, wait until the start time
while time.strftime('%H:%M:%S') < start_time:
    print(f"Waiting for start time: {start_time}")
    logging.info(f"Waiting for start time: {start_time}")
    time.sleep(1)

#run the loop while the current time is between the start and end times
while time.strftime('%H:%M:%S') >= start_time and time.strftime('%H:%M:%S') <= end_time:
    
    green_light = "01:00"
    yellow_light = "59:00"
    red_light = "00:00"

    #define the minute number and seconds that each stage begins at
    green_light_minute = datetime.strptime(green_light, "%M:%S")
    yellow_light_minute = datetime.strptime(yellow_light, "%M:%S")
    red_light_minute = datetime.strptime(red_light, '%M:%S')
    
    #convert the current time to minutes and seconds
    current_minute = datetime.strptime(datetime.now().strftime('%M:%S'), "%M:%S")

    print(current_minute)
    logging.info(f"Time: {time.strftime('%H:%M:%S')}, Date: {time.strftime('%m/%d/%Y')}")
    logging.info(f"Current minute: {current_minute}")

    if current_minute >= green_light_minute and current_minute < yellow_light_minute:
        stoplight.greenlight()
        print("Green light on")
        sleep_time = yellow_light_minute - current_minute
        
    elif current_minute >= yellow_light_minute and current_minute < red_light_minute:
        stoplight.yellowlight()
        print("Yellow light on")
        sleep_time = red_light_minute - current_minute
        
    elif current_minute >= red_light_minute or current_minute < green_light_minute:
        stoplight.redlight()
        print("Red light on")
        sleep_time = (datetime.strptime("59:59", "%M:%S") - current_minute) if current_minute >= red_light_minute else (green_light_minute - current_minute)
        

    print(f"Sleeping for {sleep_time.total_seconds()} seconds")
    logging.info(f"Sleeping for {sleep_time.total_seconds()} seconds")
    #Convert the minute value to an integer
    countdown(sleep_time.total_seconds())
    time.sleep(round((sleep_time.total_seconds()), 2))
    
    
#turn off the lights
stoplight.shutdown()
logging.info("Stoplight control script stopped at " + time.strftime('%H:%M:%S'))

