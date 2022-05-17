from django.shortcuts import render
from django.http import HttpResponse
from scapy.all import *
from codecs import encode
from .killerbee_interface import *
from killerbee import *

kb = None

def index(request):
    global kb
    template = 'hackbee/index.html'
    device_list = get_device_information()

    context = {
        'device_list': device_list,
    }
    if request.GET.get("start_channel_discovery"):
        dev_id = request.GET.get("dev_id")
        channel = request.GET.get("channel")
        if channel == "":
            channel = None
        delay = request.GET.get("delay")
        if delay == "":
            delay = 2
        scan_time = request.GET.get("scan_time")
        if scan_time == "" or int(scan_time) > 3:
            scan_time = 3
        get_open_channels(dev_id=dev_id, channel = channel, verbose=False, delay=delay, scan_time=scan_time)
        with open('/tmp/network_data.json') as f:
            network_data = json.load(f)
        print(type(network_data))
        context['stumbler_results'] = network_data

    if request.GET.get("start_zbgoodfind"):
        goodfind_results = goodfind(request)
        context['zbgoodfind_key'] = goodfind_results['zbgoodfind_key']
        context['zbgoodfind_guesses'] = goodfind_results['zbgoodfind_guesses']
        context['zbgoodfind_status'] = goodfind_results['zbgoodfind_status']

    if request.GET.get("start_zbconverter"):
        output_file, status = convert_dsna_to_pcap(request)
        if output_file == None:
            context['zbconverter_status'] = status
            context['zbconverter_output_file'] = "Error"
        else:
            context['zbconverter_status'] = status
            context['zbconverter_output_file'] = output_file
    
    if request.GET.get("start_sniffing"):
        pcap_file_path = request.GET.get("pcap_file_path")
        dev_id = request.GET.get("dev_id")
        channel = int(request.GET.get("channel"))
        packetcount = request.GET.get("packetcount")
        if packetcount == "":
            packetcount = None
        if pcap_file_path == "":
            pcap_file_path['pcap_reader'] = "Please provide pcap file path."
        else:
            killerbee_sniffer(dev_id,channel,pcap_file_path,packetcount)
            
    if request.GET.get("stop_sniffing"):
        kb.break_signal = True
    
    if request.GET.get("read_pcap"):
        pcap_file_path = request.GET.get("pcap_file_path")
        if pcap_file_path == "":
            pcap_file_path = "Provide PCAP path."
        else:
            conf.dot15d4_protocol = "zigbee"
            scapy_cap = rdpcap(pcap_file_path)
            packet_capture = []
            for packet in scapy_cap:
                try:
                    dot15d4_fcs =  {
                        "fcf_reserved_1" : packet[Dot15d4][Dot15d4FCS].fcf_reserved_1,
                        "fcf_panidcompress" : packet[Dot15d4][Dot15d4FCS].fcf_panidcompress,
                        "fcf_ackreq" : packet[Dot15d4][Dot15d4FCS].fcf_ackreq,
                        "fcf_pending" : packet[Dot15d4][Dot15d4FCS].fcf_pending,
                        "fcf_security" : packet[Dot15d4][Dot15d4FCS].fcf_security,
                        "fcf_frametype" : packet[Dot15d4][Dot15d4FCS].fcf_frametype,
                        "fcf_srcaddrmode" : packet[Dot15d4][Dot15d4FCS].fcf_srcaddrmode,
                        "fcf_framever" : packet[Dot15d4][Dot15d4FCS].fcf_framever,
                        "fcf_destaddrmode" : packet[Dot15d4][Dot15d4FCS].fcf_destaddrmode,
                        "fcf_reserved_2" : packet[Dot15d4][Dot15d4FCS].fcf_reserved_2,
                        "seqnum" : packet[Dot15d4][Dot15d4FCS].seqnum,
                        "fcs" : packet[Dot15d4][Dot15d4FCS].fcs
                        }
                except:
                    pass
                try:
                    dot15d4_data = {
                        "dest_panid" : packet[Dot15d4][Dot15d4Data].dest_panid,
                        "dest_addr" : packet[Dot15d4][Dot15d4Data].dest_addr,
                        "src_addr" : packet[Dot15d4][Dot15d4Data].src_addr
                        }
                except:
                    pass
                try:
                    zigbee_nwk = {
                        "discover_route" : packet[Dot15d4][ZigbeeNWK].discover_route,
                        "proto_version" : packet[Dot15d4][ZigbeeNWK].proto_version,
                        "frametype" : packet[Dot15d4][ZigbeeNWK].frametype,
                        "flags" : packet[Dot15d4][ZigbeeNWK].flags,
                        "destination" : packet[Dot15d4][ZigbeeNWK].destination,
                        "source" : packet[Dot15d4][ZigbeeNWK].source,
                        "radius" : packet[Dot15d4][ZigbeeNWK].radius,
                        "seqnum" : packet[Dot15d4][ZigbeeNWK].seqnum
                        }
                except:
                    pass
                try:
                    zigbee_security_header = {
                        "reserved1" : packet[Dot15d4][ZigbeeSecurityHeader].reserved1,
                        "extended_nonce" : packet[Dot15d4][ZigbeeSecurityHeader].extended_nonce,
                        "key_type" : packet[Dot15d4][ZigbeeSecurityHeader].key_type,
                        "nwk_seclevel" : packet[Dot15d4][ZigbeeSecurityHeader].nwk_seclevel,
                        "fc" : packet[Dot15d4][ZigbeeSecurityHeader].fc,
                        "source" : packet[Dot15d4][ZigbeeSecurityHeader].source,
                        "key_seqnum" : packet[Dot15d4][ZigbeeSecurityHeader].key_seqnum,
                        "data" : packet[Dot15d4][ZigbeeSecurityHeader].data
                        }
                except:
                    pass
                try:
                    data_utf = str(encode(packet[Dot15d4][ZigbeeSecurityHeader].data, "hex"), "utf-8")
                    data_mic = data_utf.split("b9")
                except:
                    pass
                
            context['pcap_content'] = scapy_cap

    return render(request, template, context = context)

def goodfind(request):
    if request.GET.get("input_pcap") != "" and request.GET.get("input_memdump") != "":
        pcap = request.GET.get("input_pcap")
        memdump = request.GET.get("input_memdump")
        key, guesses, status_code = key_search_pcap_mem(memdump, pcap)
    elif request.GET.get("input_pcap") == "" and request.GET.get("input_memdump") != "":
        key = None
        guesses = None
        status_code = "Provide PCAP path"
    elif request.GET.get("input_pcap") != "" and request.GET.get("input_memdump") == "":
        key = None
        guesses = None
        status_code = "Provide memory dump path"
    else:
        memdump = "/home/pi/Desktop/Studienarbeit_Dev/hackbee/hackbee_web/hackbee/ressources/memdump.bin"
        pcap = "/home/pi/Desktop/Studienarbeit_Dev/hackbee/hackbee_web/hackbee/ressources/zigbee-encrypted.pcap"
        key, guesses, status_code = key_search_pcap_mem(memdump, pcap)
    
    goodfind_results = {
        'zbgoodfind_key' : key,
        'zbgoodfind_guesses' : guesses,
        'zbgoodfind_status' : status_code
    }
    return goodfind_results

def convert_dsna_to_pcap(request):
    input_file_path = request.GET.get("input_convert_file_path")
    output_file_path = request.GET.get("output_convert_file_path")
    print(input_file_path)
    print(output_file_path)
    if input_file_path == "":
        status = "Please provide input file path."
    elif output_file_path == "":
        status = "Please provide output file path."
    else:
        status = convert_dsna_to_pcap_file(input_file_path, output_file_path)

    if status != "Success":
        output_file_path = None
    
    return output_file_path, status

def killerbee_sniffer(dev_id, channel, pcap_file_path, count):
    global kb
    with KillerBee(device=dev_id) as kb:
        try:
            kb.set_channel(channel, 0)
            kb.break_signal = False
        except ValueError as e:
            return "Could not set channel."
        with PcapDumper(DLT_IEEE802_15_4, pcap_file_path, False) as pd:
            rf_freq_mhz = kb.frequency(channel, 0) / 1000.0
            packetcount = 0
            if count is not None:
                count = int(count)
            while count != packetcount:
                # Wait for the next packet
                packet = kb.pnext()
                if packet != None:
                    packetcount+=1
                    pd.pcap_dump(packet['bytes'], ant_dbm=packet['dbm'], freq_mhz=rf_freq_mhz)
                
                if kb.break_signal:
                    break
                    
            kb.sniffer_off()
            print(("{0} packets captured".format(packetcount)))