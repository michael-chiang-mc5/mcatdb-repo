from django.db import models
from django.contrib.auth.models import User
from Test.models import Tag

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    alias = models.TextField(blank=True,null=True)
    tags_include = models.ManyToManyField(Tag, blank=True, related_name="tags_include")  # to access tags_include from UserProfile instance, userProfile.tags_include.all()
    tags_exclude = models.ManyToManyField(Tag, blank=True, related_name="tags_exclude")  # to access tags_include from UserProfile instance, userProfile.tags_exclude.all()

    def __str__(self):
        return str(self.user)
    def getName(self):
        if self.alias:
            return self.alias
        else:
            return user.get_username()
