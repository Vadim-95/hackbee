import os
import json
from killerbee import *

def get_device_information():
    device_information = show_dev()
    print(device_information)
    return device_information

def get_open_channels(dev_id, channel, verbose=False, file_path=None, delay=2, scan_time=3):
    '''
    Runs killerbees tool zbstumbler. 
    Structure of network_data =
    [{
        'panid': '0x1234', 
        'source': '0x0000', 
        'extpanid': '00:xx:xx:xx:xx:xx:xx:xx', 
        'stackprofile': <'Network Specific'|'ZigBee Enterprise'|'ZigBee Enterprise'>
        'stackversion': <'ZigBee Prototype'|'ZigBee 2004'|'ZigBee 2006/2007'>
        'channel': <11-25>
    }]
    TODO:
    Add file_path for JSON and make it a parameter (not optional).
    Add support for verbose by displaying tool output on web interface in realtime.
    '''
    if not dev_id:
        return "Please provide Device ID/Interface."
    elif not channel:
        return "Please provide channel."
    if verbose:
         os.system("sudo zbstumbler -i {0} -c {1} -s {2} -w {3} -v -d {4}".format(dev_id, channel, delay, file_path, scan_time))
    else:
        os.system("sudo zbstumbler -i {0} -c {1} -s {2} -w {3} -d {4}".format(dev_id, channel, delay, file_path, scan_time))

    with open('/tmp/network_data.json', 'w') as f:
        network_data = json.load(f)
        
    print(network_data)