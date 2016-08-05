from django.shortcuts import render

def adminPanel(request):
    #if not request.user.is_superuser: # TODO: add back in
    #    return HttpResponse("You are not a superuser")
    context = {}
    return render(request, 'Test/adminPanel.html', context)
