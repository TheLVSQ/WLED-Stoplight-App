import logging
import json
import logging
from stoplight_main import activate_color

#create a logging object
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_light_info():
    #Open the config file
    with open('wled_config.json') as f:
        config = json.load(f)

    #log the config data
    logger.info(f"Config data: {config}")

    return config['server_ip']

def yellowlight(server_ip):
        on_segment = 2
        off_segments = [1, 3]
        colors= ["ffffff", "000000", "000000"]
        activate_color(server_ip, on_segment, off_segments, colors)

if __name__ == "__main__":
    
    led_ip = get_light_info()

    yellowlight(led_ip)
