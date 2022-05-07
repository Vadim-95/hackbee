from django.shortcuts import render
from django.http import HttpResponse
from .killerbee_interface import *

def index(request):
    template = 'hackbee/index.html'
    device_list = get_device_information()

    context = {
        'device_list': device_list,
    }
    if request.GET.get("start_channel_discovery"):
        dev_id = request.GET.get("dev_id")
        channel = request.GET.get("channel")
        delay = request.GET.get("delay")
        if delay == "":
            delay = 2
        scan_time = request.GET.get("scan_time")
        if scan_time == "" or int(scan_time) > 3:
            scan_time = 3
        stumbler_results = get_open_channels(dev_id=dev_id, channel = channel, verbose=False, delay=delay, scan_time=scan_time)
        context['stumbler_results'] = stumbler_results

    if request.GET.get("start_zbgoodfind"):
        goodfind_results = goodfind(request)
        context['zbgoodfind_key'] = goodfind_results['zbgoodfind_key']
        context['zbgoodfind_guesses'] = goodfind_results['zbgoodfind_guesses']
        context['zbgoodfind_status'] = goodfind_results['zbgoodfind_status']

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