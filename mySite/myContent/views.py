from django.shortcuts import render
from django.http import HttpResponse
from UserProfile.models import UserProfile
from UserProfile.views import new_user

def index(request):
    if request.user.is_authenticated():
        userProfileExists = UserProfile.exists(request.user)
        if not userProfileExists:
            user = request.user
            userprofile = UserProfile(user=user,alias=user.username)
            userprofile.save()
    context = {}
    return render(request, 'myContent/questionOfTheDay.html', context)


def questionOfTheDay(request):
    context = {}
    return render(request, 'myContent/questionOfTheDay.html', context)
