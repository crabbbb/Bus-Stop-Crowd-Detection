from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from backend.utils import getDBInfo
import os

def test_mongo_config(request):
    mongo_uri, db_name = getDBInfo()

    return JsonResponse({
        "MongoDB URI": mongo_uri,
        "Database Name": db_name
    })