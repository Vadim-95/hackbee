from django.shortcuts import render
from django.http import HttpResponse

import datetime
from .models import *

def start_report(stime,etime):
    goodfind= Zbgoodfind.objects.all().filter(start_time__gte=stime,start_time__lte=etime).values()
    zconvert = Zbconvert.objects.all().filter(start_time__gte=stime,start_time__lte=etime).values()
    zbreplay = Zbreplay.objects.all().filter(start_time__gte=stime,start_time__lte=etime).values()
    context = {
        'gfind' : goodfind,
        'zconvert' : zconvert,
        'zbreplay' : zbreplay
    }
    print(zconvert)
    return context





