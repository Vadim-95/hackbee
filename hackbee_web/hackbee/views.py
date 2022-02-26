from django.shortcuts import render
from django.http import HttpResponse
from .killerbee_interface import *

def index(request):
    template = 'hackbee/index.html'
    device_list = get_device_information()
    # get_open_channels("1:3","15",scan_time=3)
    context = {
        'device_information': device_list,
    }    
    return render(request, template, context = context)
