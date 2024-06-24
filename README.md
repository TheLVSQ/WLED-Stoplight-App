# WLED Stoplight App

A simple custom app to control a WLED lightstrip in a friend's coffee shop.
## Installation

1. Clone the repo

2. Run the config_creator.py script to generate the config variables:

```bash 
python config_creator.py
```

3. Edit your cron schedule to run the lights at specific times

```bash
crontab -e
```

example:
'''
0 * * * * cd ~/WLED-Stoplight-App && stoplight-red.py
'''

The light will change to the color of the script called at the specific time.


That's it! The app should be running now.

