from django.db import models
from Test.models import *
from django.db.models import Max
import datetime

class QuestionOfTheDay(models.Model):
    questionContainer = models.ForeignKey(QuestionContainer)
    order = models.FloatField()
    @staticmethod
    def max_order():
        questionsOfTheDay = QuestionOfTheDay.objects.all()
        if len(questionsOfTheDay)==0:
            return 0
        else:
            max_order = questionsOfTheDay.aggregate(Max('order'))['order__max']
            return max_order
    @staticmethod
    def get_questionOfTheDay():
        base_time = datetime.datetime(2016, 8, 8, 0, 0, 0, 0) # calculate time since 8-8-2016
        today = datetime.datetime.today()
        days_elapsed = (today - base_time).days
        num_questionsOfTheDay = len(QuestionOfTheDay.objects.all())
        index = days_elapsed % num_questionsOfTheDay
        return QuestionOfTheDay.objects.order_by('order')[index]
