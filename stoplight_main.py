import requests
import json
import logging
import time

# Set up logging at info level
logging.basicConfig(filename='stoplight.log', level=logging.INFO) 


def activate_color(server_ip, on_segment, off_segments, col_list):
    
    data_on = {'id': on_segment, "on": True, "col": col_list}
    data_off = [{'id': seg_id, "on": False} for seg_id in off_segments]
    
    # Update the WLED strip
    url = "http://" + server_ip + "/json/state"
    payload = json.dumps({
        "on": True,
        "bri": 255,
        "transition": 0,
        "seg": [data_on, data_off[0], data_off[1]]
    })
    headers = {
        'content-Type': 'application/json'
    }
    
    response = requests.post(url, data=payload, headers=headers)
    
    #log the time and the response from the WLED strip
    logging.info(f"Time: {time.strftime('%H:%M:%S')}, Response: {response.json()}")
    
    print(response.json())