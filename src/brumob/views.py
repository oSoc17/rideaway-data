# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os.path
# Create your views here.

#def index(request):
#     return HttpResponse("hello world from poll index")
def index(request):
    template = loader.get_template('brumob/index.html')
    context={}
    return HttpResponse(template.render(context,request))
def downloads(request):
    template = loader.get_template('brumob/download.html')

    #
    route_list=["1","1a","1b","2","2a","2b","3","3a","3b","4","5","5a","5b","MM","6","6a","6b","7","8","SZ","SZa","SZb","KC","9","9a","9b","10","10a","10b","11","11a","11b","12","12a","12b","MM","MMa","MMb","PP",]
    
    context={
    'route_list':route_list,
    }
   
    return HttpResponse(template.render(context,request))


def downloaditem(request,route):
    #template = loader.get_template('brumob/download.html')
    #context={}
    print('hello')
    BASE = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(BASE, "files/textfile.txt"), 'rb') as fh:
        response = HttpResponse(fh, content_type="application/text") 
        response["Content-disposition"] = 'attachment; filename="textfile.txt"'
        return response
