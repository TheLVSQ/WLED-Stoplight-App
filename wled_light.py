"""_summary_
"""

import logging, requests, json


class Wled_Strip():
    def __init__ (self, ip, start_time, end_time):
        # Initialize the WLED strip
            self.server_ip = ip
            self.start_time = start_time
            self.end_time = end_time
            
    
    def update(self, on_segment, off_segments, col_list):
        
        data_on = {'id': on_segment, "on": True, "col": col_list}
        data_off = [{'id': seg_id, "on": False} for seg_id in off_segments]

        # Update the WLED strip
        url = "http://" + self.server_ip + "/json/state"
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
        print(response.json())

    def redlight(self):
        brightness = 255
        on_segment = 1
        off_segments = [2, 3]
        colors= ["f00101", "000000", "000000"]
        self.update(on_segment, off_segments, colors)

    def yellowlight(self):
        on_segment = 2
        off_segments = [1, 3]
        colors= ["f0ec01", "000000", "000000"]
        self.update(on_segment, off_segments, colors)

    def greenlight(self):
        on_segment = 3
        off_segments = [1, 2]
        colors = ["37e704", "000000", "000000"]
        self.update(on_segment, off_segments, colors)

    def get_state(self):
        url = "http://" + self.server_ip + "/json/state"
        response = requests.get(url)
        return response.json()
    
    def shutdown(self):
        segments = [1,2,3]
        data_off = [{'id': seg_id, "on": False} for seg_id in segments]

        # Turn off the WLED strip
        url = "http://" + self.server_ip + "/json/state"
        payload = json.dumps({
            "on": True,
            "bri": 255,
            "transition": 0,
            "seg": [data_off[0], data_off[1], data_off[2]]
        })
        headers = {
            'content-Type': 'application/json'
        }
        response = requests.post(url, data=payload, headers=headers)
        return response.json()