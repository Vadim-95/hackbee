from django.shortcuts import render
from django.http import HttpResponse
from .killerbee_interface import *

def index(request):
    get_device_information()
    #get_open_channels()
    get_open_channels("1:3","15",scan_time=3)
    return HttpResponse(
        "Hello"
    )
