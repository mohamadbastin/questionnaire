from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    picture = models.CharField(max_length=1000000000, null=True, blank=True)


class Time(models.Model):
    hour = models.TimeField()
    form = models.ForeignKey('Form', on_delete=models.CASCADE, related_name='time')


class Form(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="form")
    name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    is_private = models.BooleanField(default=False)
    estimated_time = models.IntegerField(null=True)
    is_repeated = models.BooleanField(default=False)
    duration_days = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)


class Request(models.Model):
    class Meta:
        unique_together = ['sender', 'form']

    choices = [("ACC", "accepted"), ("REJ", "rejected"), ("WIT", "waiting")]
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="request")
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="request")
    status = models.CharField(max_length=128, choices=choices, default="WIT")
    is_read = models.BooleanField(default=False)


class AnsweredForm(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="answered_form")
    participant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="answered_form")
    date = models.DateTimeField(auto_now_add=True, )
    is_read = models.BooleanField(default=False)


class Answer(models.Model):
    answered_form = models.ForeignKey(AnsweredForm, on_delete=models.CASCADE, related_name="answer")
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="answer")
    text = models.CharField(max_length=1024, null=True, blank=True)
    number = models.FloatField(null=True, blank=True)


class Question(models.Model):
    class Meta:
        unique_together = ["number", "form"]

    number = models.IntegerField(null=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="Question")
    text = models.CharField(max_length=1024)


class TextQuestion(Question):
    description = models.CharField(max_length=1024, null=True, blank=True)


class RangeQuestion(Question):
    start = models.IntegerField()
    end = models.IntegerField()
    start_text = models.CharField(max_length=128, null=True, blank=True)
    end_text = models.CharField(max_length=128, null=True, blank=True)


class ChoiceQuestion(Question):
    choices = [("MA", "multiple answer"), ("SA", "single answer")]
    type = models.CharField(max_length=10, choices=choices)


class Choice(models.Model):
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE, related_name="choice")
    text = models.CharField(max_length=256)


class AnswerChoiceRelation(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="choice")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="answer")
