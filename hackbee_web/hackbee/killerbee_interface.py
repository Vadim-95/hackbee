import os
import json
import killerbee

def get_device_information():
    device_information = killerbee.show_dev()
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

    with open('/tmp/network_data.json') as f:
        network_data = json.load(f)

def key_search_pcap_mem(memdump, pcap):
    try:
        os.system("sudo zbgoodfind -r {0} -f {1} ".format(pcap, memdump))
        with open('/tmp/zbgoodfind_result.json') as f:
            zbgoodfind_result = json.load(f)
        key = zbgoodfind_result["key"]
        guesses = zbgoodfind_result["guesses"]
        status_code = "Success"
    except Exception as e:
        print(e)
        key = None
        guesses = None
        status_code = "Please provide correct file paths."
        
    return key, guesses, status_code