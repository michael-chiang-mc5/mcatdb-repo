from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return questionOfTheDay(request)

def questionOfTheDay(request):
    context = {}
    return render(request, 'myContent/questionOfTheDay.html', context)
