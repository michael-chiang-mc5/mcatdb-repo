from django.db import models

class Passage(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    adminNotes = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.text
    def edit(self,text):
        self.text = text

class Question(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    hidden = models.BooleanField(default=True)
    passage = models.ForeignKey(Passage, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    adminNotes = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.text
    def edit(self,text):
        self.text = text

class Answer(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    question = models.ForeignKey(Question)
    correct = models.BooleanField(default=False)
    explanation = models.TextField()
    adminNotes = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.text

class Tag(models.Model):
    text = models.CharField(max_length=255, unique=True)
    questions  = models.ManyToManyField(Question, blank=True, related_name="tags")  # to access tags from Question instance, question.tags.all()
    def __str__(self):
        return self.text
    # saves a new class object if one does not already exist
    def newTag(text):
        tags = Tag.objects.filter(text=text)
        if len(tags)==0:
            tag = Tag(text=text)
            tag.save()
