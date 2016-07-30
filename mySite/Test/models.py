from django.db import models
import random
import datetime

class Passage(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    adminNotes = models.TextField()
    def __str__(self):
        return self.text
    def edit(self,text):
        self.text = text

# Question includes both passage-based questions and standalone questions
class Question(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    hidden = models.BooleanField(default=True)
    passage = models.ForeignKey(Passage, blank=True, null=True) # null if a standalone question
    notes = models.TextField(blank=True, null=True)
    adminNotes = models.TextField()
    def __str__(self):
        return self.text
    def edit(self,text):
        self.text = text
    # returns dictionary with fields:
    #   type: passage or standaloneQuestion
    #   pk: id of passage or standaloneQuestion
    @classmethod
    def get_random_passage_or_standaloneQuestion(self,user):
        # filter by include/exclude tags
        tags_include = user.userprofile.tags_include.all()
        tags_exclude = user.userprofile.tags_exclude.all()
        if len(tags_include) > 0:
            questions = Question.objects.all()
            for tag_include in tags_include:
                questions = questions.filter(tags__in=[tag_include])
        else:
            questions = Question.objects.all()
        questions = questions.exclude(tags__in=tags_exclude)
        # filter by question creation date
        if user.userprofile.mindate is None:
            mindate = datetime.datetime.min
        else:
            mindate = user.userprofile.mindate
        if user.userprofile.maxdate is None:
            maxdate = datetime.datetime.max
        else:
            maxdate = user.userprofile.maxdate
        questions = questions.filter(time__range=[mindate, maxdate])

        # get passages and standalone questions
        passages = Passage.objects.filter(question__in=questions).distinct()
        standaloneQuestions = questions.exclude(passage__isnull=False)
        # randomly choose passage/standaloneQuestion
        random_integer = random.randint(0,passages.count()+standaloneQuestions.count()-1)
        if random_integer < passages.count():
            return {'type':'passage','pk':passages[random_integer].pk}
        else:
            return {'type':'standaloneQuestion','pk':standaloneQuestions[random_integer-passages.count()].pk}
    def is_standalone(self):
        if self.passage == None:
            return True

class Answer(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    question = models.ForeignKey(Question)
    correct = models.BooleanField(default=False)
    explanation = models.TextField()
    def __str__(self):
        return self.text

class Tag(models.Model):
    text = models.CharField(max_length=255, unique=True)
    questions  = models.ManyToManyField(Question, blank=True, related_name="tags")  # to access tags from Question instance, question.tags.all()
    def __str__(self):
        return self.text
    # saves a new class object if one does not already exist
    @classmethod
    def newTag(self,text):
        tags = Tag.objects.filter(text=text)
        if len(tags)==0:
            tag = Tag(text=text)
            tag.save()
