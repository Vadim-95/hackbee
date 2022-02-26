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
