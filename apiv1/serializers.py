from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ['hour']


class FormSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    time = TimeSerializer(many=True)

    class Meta:
        model = Form
        fields = [field.name for field in model._meta.fields] + ['time']


class Request(serializers.ModelSerializer):
    form = FormSerializer()
    sender = ProfileSerializer()

    class Meta:
        model = Request
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    # form = FormSerializer()

    class Meta:
        model = Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = "__all__"


class AnsweredFormSerializer(serializers.ModelSerializer):
    # form = FormSerializer()
    # participant = ProfileSerializer()
    answer = AnswerSerializer(many=True)

    class Meta:
        model = AnsweredForm
        fields = [field.name for field in model._meta.fields] + ["answer"]


class TextQuestionSerializer(QuestionSerializer):
    class Meta:
        model = TextQuestion
        fields = "__all__"


class RangeQuestionSerializer(QuestionSerializer):
    class Meta:
        model = RangeQuestion
        fields = "__all__"


class ChoiceQuestionSerializer(QuestionSerializer):
    class Meta:
        model = ChoiceQuestion
        fields = "__all__"


class ChoiceSerializer(serializers.ModelSerializer):
    question = ChoiceQuestionSerializer()

    class Meta:
        model = Choice
        fields = "__all__"


class AnswerChoiceRelationSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer()
    choice = ChoiceSerializer()

    class Meta:
        model = AnswerChoiceRelation
        fields = "__all__"
