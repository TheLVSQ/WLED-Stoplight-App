import logging
import requests
import json
import time
import logging
from stoplight_main import activate_color

logger = logging.basicConfig(filename='stoplight_red.log', level=logging.INFO)

def get_light_info():
    #Open the config file
    with open('wled_config.json') as f:
        config = json.load(f)

    logger.info(f"config reqtrieved: {config}")

    return config['server_ip']

def redlight(server_ip):
        on_segment = 1
        off_segments = [2, 3]
        colors= ["f00101", "000000", "000000"]
        activate_color(on_segment, off_segments, colors)

if __name__ == "__main__":
    
    led_ip = get_light_info()

    redlight(led_ip)
