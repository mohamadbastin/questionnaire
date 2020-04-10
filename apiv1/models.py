import json

import requests
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


class Message(models.Model):
    to = models.CharField(max_length=15)
    token = models.CharField(max_length=100000)
    token2 = models.CharField(max_length=1000000, null=True, blank=True)
    token3 = models.CharField(max_length=1000000, null=True, blank=True)

    block_code = models.IntegerField(blank=True, null=True)

    last_try = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.to) + " : " + str(self.token)


class Operator(models.Model):
    name = models.CharField(max_length=255)
    template = models.CharField(max_length=255)

    # username = models.CharField(max_length=255, verbose_name=_("Username"), help_text=_("User name given by operator"
    # password = models.CharField(max_length=255, verbose_name=_("Password"), help_text=_("Password given by operator"))

    # sender = models.CharField(max_length=15, verbose_name=_("Sender Phone Number"),
    #                           help_text=_("The operator phone number"))

    # retry_gap_time = models.IntegerField(verbose_name=_("Retry Gap Time"),
    #                                      help_text=_("Time in minutes before you can try to send a message again"))

    api_endpoint = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    def send_message(self, message):

        # api = furl(self.api_endpoint)
        #
        # api.args['uname'] = self.username
        # api.args['pass'] = self.password
        # api.args['from'] = self.sender
        # api.args['msg'] = message.message
        # api.args['to'] = message.to

        # check for retry gap
        # now = timezone.now()
        # if message.last_try is None:
        #     message.last_try = now - timezone.timedelta(minutes=self.retry_gap_time * 2)

        # if now - message.last_try >= timezone.timedelta(minutes=self.retry_gap_time):
        # eligible to retry

        # message.last_try = now
        data = {"receptor": message.to, "template": self.template, "token": message.token, "token2": message.token2,
                "token3": message.token3}
        r = requests.post(self.api_endpoint, data=data)

        try:
            # print(r)
            # print(1)
            # print(json.loads(r.text))
            # print(2)
            block_code = json.loads(r.text)[1]["entries"][0]["messageid"]
            message.block_code = block_code
        except:
            err = json.loads(r.text)
            return {'status': 'OK', 'msg': err[1]}

        # tdo: fix bug on retry gap if fails
        message.save()

        return {'status': 'OK', 'msg': "Message Sent"}

    # else:
    #     return {'status': 'NOK', 'msg': _("try again later")}
    # not eligible to retry
