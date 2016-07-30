from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import *
from django.contrib.auth import logout
from Test.models import Tag
from datetime import datetime

def new_user(request):
    user = request.user
    userprofile = UserProfile(user=user,alias=user.username)
    userprofile.save()
    return HttpResponseRedirect(reverse('myContent:index'))

def editProfileInterface(request):
    tags = Tag.objects.extra( select={'lower_text': 'lower(text)'}).order_by("lower_text").all() # tags sorted in alphabetical order
    for tag in tags:
        tag.include = tag in request.user.userprofile.tags_include.all()
        tag.exclude = tag in request.user.userprofile.tags_exclude.all()
    mindate = request.user.userprofile.mindate
    maxdate = request.user.userprofile.maxdate
    context = {'tags':tags,'mindate':mindate,'maxdate':maxdate}
    return render(request,'UserProfile/editProfileInterface.html',context)
def editAlias(request):
    user = request.user
    user.userprofile.alias = request.POST.get('form_text')
    user.userprofile.save()
    return HttpResponseRedirect(reverse('UserProfile:editProfileInterface'))
# User specifies which sorts of questions (tags) will show up with "random question"
# is selected
def editUserTags(request):
    user = request.user
    tags = Tag.objects.all()
    for tag in tags:
        # Tag was checkmarked (either include or exclude)
        if request.POST.get(tag.text,False):
            if request.POST.get(tag.text) == "include":
                user.userprofile.tags_include.add(tag)
                user.userprofile.tags_exclude.remove(tag)
            elif request.POST.get(tag.text) == "exclude":
                user.userprofile.tags_include.remove(tag)
                user.userprofile.tags_exclude.add(tag)
        # No tag checkmark
        else:
            user.userprofile.tags_include.remove(tag)
            user.userprofile.tags_exclude.remove(tag)
    return HttpResponseRedirect(reverse('UserProfile:editProfileInterface'))
# User specifies which sorts of questions (dates) will show up with "random question"
# is selected
def editUserDates(request):
    user = request.user
    mindate = request.POST.get("mindate",False)
    maxdate = request.POST.get("maxdate",False)

    try:
        mindate = datetime.strptime(mindate , '%m/%d/%Y')
    except:
        user.userprofile.mindate = None
    else:
        user.userprofile.mindate = mindate
    try:
        maxdate = datetime.strptime(maxdate , '%m/%d/%Y')
    except:
        user.userprofile.maxdate = None
    else:
        user.userprofile.maxdate = maxdate
    user.userprofile.save()

    return HttpResponseRedirect(reverse('UserProfile:editProfileInterface'))
