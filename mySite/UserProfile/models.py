from django.db import models
from django.contrib.auth.models import User
from Test.models import Tag

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    alias = models.TextField(blank=True,null=True)
    tags_include = models.ManyToManyField(Tag, blank=True, related_name="tags_include")  # to access tags_include from UserProfile instance, userProfile.tags_include.all()
    tags_exclude = models.ManyToManyField(Tag, blank=True, related_name="tags_exclude")  # to access tags_include from UserProfile instance, userProfile.tags_exclude.all()
    seeAdminTools = models.BooleanField(default=False)
    mindate = models.DateTimeField(blank=True,null=True) # when showing random questions, only include questions created between mintime, maxtime
    maxdate = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return str(self.user)
    def getName(self):
        if self.alias:
            return self.alias
        else:
            return user.get_username()
    @classmethod
    def exists(self,user_obj):
        try:
            UserProfile.objects.get(user=user_obj)
        except:
            return False
        else:
            return True
