import os
import json
import killerbee

def get_device_information():
    device_information = killerbee.show_dev()
    return device_information

def get_open_channels(dev_id, channel, verbose=False, delay=2, scan_time=3):
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
    if channel is None:
        os.system("sudo zbstumbler -i {0} -s {1} -d {2}".format(dev_id, delay, scan_time))
    else:
        os.system("sudo zbstumbler -i {0} -c {1} -s {2} -d {3}".format(dev_id, channel, delay, scan_time))

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

def convert_dsna_to_pcap_file(input_file_path, output_file_path):
    try:
        os.system("sudo zbconverter -i {0} -o {1} ".format(input_file_path, output_file_path))
        status_code = "Success"
    except Exception as e:
        print(e)
        status_code = "Conversion failed."
    
    return status_code