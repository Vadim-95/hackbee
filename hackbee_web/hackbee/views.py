from django.shortcuts import render
from django.http import HttpResponse
import killerbee_interface as kb

def index(request):
    kb.get_device_information()
    kb.get_open_channels()
    return HttpResponse(
        "Hello"
    )