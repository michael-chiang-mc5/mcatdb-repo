from django.shortcuts import render
from django.http import HttpResponse
from UserProfile.models import UserProfile
from UserProfile.views import new_user

# front page of mcatDB. Displays a random "Question of the Day"
def index(request):
    if request.user.is_authenticated():
        userProfileExists = UserProfile.exists(request.user)
        if not userProfileExists:
            user = request.user
            userprofile = UserProfile(user=user,alias=user.username)
            userprofile.save()

    request.user.is_superuser = True
    context = {'passage':True}
    return render(request, 'myContent/frontpage.html', context)
