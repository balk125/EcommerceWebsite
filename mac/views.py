from django.shortcuts import render
from django.http import HttpResponse
def home(request):
    return HttpResponse('this is tutorial 25')