import wled_light as wled 
import time, json, requests, sys, os
from datetime import datetime

#open the config json file
with open('wled_config.json') as json_file:
    config = json.load(json_file)

#create a new instance of the WLED class
stoplight = wled.Wled_Strip(config['server_ip'], config['start_time'], config['end_time'])

#This script needs to run in a loop during the start and end times from the config file:
start_time = config['start_time']
end_time = config['end_time']

#run the loop while the current time is between the start and end times
while time.strftime('%H:%M:%S') >= start_time and time.strftime('%H:%M:%S') <= end_time:
    
    green_light = "00:00"
    yellow_light = "55:00"
    red_light = "58:00"

    #define the minute number and seconds that each stage begins at
    green_light_minute = datetime.strptime(green_light, "%M:%S")
    yellow_light_minute = datetime.strptime(yellow_light, "%M:%S")
    red_light_minute = datetime.strptime(red_light, '%M:%S')
    
    #convert the current time to minutes and seconds
    current_minute = datetime.strptime(datetime.now().strftime('%M:%S'), "%M:%S")

    print(current_minute)

    if current_minute >= yellow_light_minute and current_minute < red_light_minute:
        stoplight.yellowlight()
        print("Yellow light on")
        sleep_time = red_light_minute - current_minute
    elif current_minute >= red_light_minute:
        stoplight.redlight()
        print("Red light on")
        sleep_time = datetime.strptime("59:59", "%M:%S") - current_minute
    elif current_minute >= green_light_minute and current_minute < yellow_light_minute:
        stoplight.greenlight()
        print("Green light on")
        #subtract current minute and second from the current hour and 55 minutes
        sleep_time = yellow_light_minute - current_minute  # Sleep until the next hour

    
    
    print(f"Sleeping for {sleep_time.total_seconds()} seconds")
    #Convert the minute value to an integer
    time.sleep(round((sleep_time.total_seconds()), 2))
    
#turn off the lights
stoplight.shutdown()


