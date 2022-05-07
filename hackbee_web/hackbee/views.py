from django.shortcuts import render
from django.http import HttpResponse
from .killerbee_interface import *

def index(request):
    template = 'hackbee/index.html'
    device_list = get_device_information()
    for device in device_list:
        print(device[0])
    # get_open_channels("1:3","15",scan_time=3)
    context = {
        'device_list': device_list,
    }    
    return render(request, template, context = context)

def goodfind(request):
    if request.POST.get("start_zbgoodfind"):
        if request.POST.get("input_pcap") is not None and request.POST.get("input_memdump") is not None:
            pcap = request.POST.get("input_pcap")
            memdump = request.POST.get("input_memdump")
            key, guesses, status_code = key_search_pcap_mem(memdump, pcap)
        elif request.POST.get("input_pcap") is None and request.POST.get("input_memdump") is not None:
            key = None
            guesses = None
        elif request.POST.get("input_pcap") is not None and request.POST.get("input_memdump") is None:
            key = None
            guesses = None
        else:
            memdump = "/home/pi/Desktop/Studienarbeit_Dev/hackbee/hackbee_web/hackbee/ressources/memdump.bin"
            pcap = "/home/pi/Desktop/Studienarbeit_Dev/hackbee/hackbee_web/hackbee/ressources/zigbee-encrypted.pcap"
            key, guesses, status_code = key_search_pcap_mem(memdump, pcap)
    
    goodfind_results = {
        'key' : key,
        'guesses' : guesses,
        'status' : status_code
    }
    return render(request, "hackbee/index.html", context = goodfind_results)