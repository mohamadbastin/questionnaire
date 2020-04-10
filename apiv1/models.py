from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    picture = models.CharField(max_length=1000000000, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


class Time(models.Model):
    hour = models.CharField(max_length=30)
    form = models.ForeignKey('Form', on_delete=models.CASCADE, related_name='time')

    def __str__(self):
        return str(self.hour) + " " + str(self.form)


class Form(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="form")
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=2048)
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    is_private = models.BooleanField(default=False)
    estimated_time = models.IntegerField(null=True)
    is_repeated = models.BooleanField(default=False)
    duration_days = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name) + " " + str(self.author)


class FormRequest(models.Model):
    class Meta:
        unique_together = ['sender', 'form']

    choices = [("ACC", "accepted"), ("REJ", "rejected"), ("WIT", "waiting")]
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="form_request")
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="form_request")
    status = models.CharField(max_length=128, choices=choices, default="WIT")
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sender) + " " + str(self.form)


class AnsweredForm(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="answered_form")
    participant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="answered_form")
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.form) + " " + str(self.participant)


class Answer(models.Model):
    answered_form = models.ForeignKey(AnsweredForm, on_delete=models.CASCADE, related_name="answer")
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="answer")
    text = models.CharField(max_length=1024, null=True, blank=True)
    number = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.answered_form) + " " + str(self.question)


class Question(models.Model):
    class Meta:
        unique_together = ["text", "form"]

    number = models.IntegerField(null=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="question")
    text = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024, null=True, blank=True)
    type = models.CharField(max_length=10, choices=[("text", "text"), ("choice", "choice"), ("range", "range")],
                            null=True)

    def __str__(self):
        return str(self.number) + "." + str(self.text) + str(self.form)


class TextQuestion(Question):
    # description = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return str(self.text)


class RangeQuestion(Question):
    start = models.IntegerField()
    end = models.IntegerField()
    start_text = models.CharField(max_length=128, null=True, blank=True)
    end_text = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return str(self.start) + ":" + str(self.start_text) + "-" + str(self.end) + ":" + str(self.end_text)


class ChoiceQuestion(Question):
    choices = [("MA", "multiple answer"), ("SA", "single answer")]
    choice_type = models.CharField(max_length=10, choices=choices)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE, related_name="choice")
    text = models.CharField(max_length=256)

    def __str__(self):
        return str(self.question) + str(self.text)


class AnswerChoiceRelation(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="choice")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="answer")

    def __str__(self):
        return str(self.answer) + str(self.choice)
