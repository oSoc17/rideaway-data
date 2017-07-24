# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os.path
import json

# Create your views here.

def index(request):
    template = loader.get_template('brumob/index.html')
    route_list = ["1", "1a", "1b", "2", "2a", "2b", "3", "3a", "3b", "4", "4a", "4b", "5", "5a", "5b", "6", "6a",
                  "6b", "7", "8", "9", "9a", "9b", "10", "10a", "10b", "11", "11a", "11b", "12", "12a", "12b", "SZ",
                  "SZa", "SZb", "CK", "MM", "MMa", "MMb", "PP", "A", "B", "C"]

    context = {
        'route_list': route_list,
        'routes': json.dumps(route_list)
    }

    return HttpResponse(template.render(context, request))


def download_route(request, route):
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "static/brumob/data/routes/" + str(route)), 'rb') as fh:
        response = HttpResponse(fh, content_type="application/vnd.geo+json")
        response["Access-Control-Allow-Origin"] = "*"
        return response


def download_output(request, route):
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "static/brumob/data/output/" + str(route)), 'rb') as fh:
        response = HttpResponse(fh, content_type="application/vnd.geo+json")
        response["Access-Control-Allow-Origin"] = "*"
        return response


def download_network(request):
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "static/brumob/data/network.geojson"), 'rb') as fh:
        response = HttpResponse(fh, content_type="application/vnd.geo+json")
        response["Access-Control-Allow-Origin"] = "*"
        return response
