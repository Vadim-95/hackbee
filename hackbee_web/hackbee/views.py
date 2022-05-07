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
    if request.POST.get("start_zbgoodfind"):
        goodfind_results = goodfind(request)
        context['zbgoodfind_key'] = goodfind_results['zbgoodfind_key']
        context['zbgoodfind_guesses'] = goodfind_results['zbgoodfind_guesses']
        context['zbgoodfind_status'] = goodfind_results['zbgoodfind_status']
        
    return render(request, template, context = context)

def goodfind(request):
    if request.POST.get("input_pcap") != "" and request.POST.get("input_memdump") != "":
        pcap = request.POST.get("input_pcap")
        memdump = request.POST.get("input_memdump")
        key, guesses, status_code = key_search_pcap_mem(memdump, pcap)
    elif request.POST.get("input_pcap") == "" and request.POST.get("input_memdump") != "":
        key = None
        guesses = None
        status_code = "Provide PCAP path"
    elif request.POST.get("input_pcap") != "" and request.POST.get("input_memdump") == "":
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