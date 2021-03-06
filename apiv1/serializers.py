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


class RequestSerializer(serializers.ModelSerializer):
    form = FormSerializer()
    sender = ProfileSerializer()

    class Meta:
        model = FormRequest
        fields = "__all__"


class ChoiceSerializer(serializers.ModelSerializer):
    # question = ChoiceQuestionSerializer()

    class Meta:
        model = Choice
        fields = ["id", "text"]


class AnswerChoiceRelationSerializer(serializers.ModelSerializer):
    # answer = AnswerSerializer()
    choice = ChoiceSerializer()

    class Meta:
        model = AnswerChoiceRelation
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    # form = FormSerializer()

    class Meta:
        model = Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    choice = AnswerChoiceRelationSerializer(many=True)

    class Meta:
        model = Answer
        fields = ['pk', 'answered_form', 'question', 'text', 'number', 'choice']


class AnsweredFormSerializer(serializers.ModelSerializer):
    # form = FormSerializer()
    participant = ProfileSerializer()
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
    choice = ChoiceSerializer(many=True)

    class Meta:
        model = ChoiceQuestion
        fields = ["id", "number", "form", "text", "description", "type", "choice_type", "choice"]


class AnswerChoiceRelationSerializer(serializers.ModelSerializer):
    # answer = AnswerSerializer()
    choice = ChoiceSerializer()

    class Meta:
        model = AnswerChoiceRelation
        fields = "__all__"


class MyQuestionSerializer(serializers.Serializer):
    question = serializers.SerializerMethodField()

    def get_question(self, instance):
        if instance.type == "text":
            serializer = TextQuestionSerializer
        elif instance.type == "range":
            serializer = RangeQuestionSerializer
        elif instance.type == "choice":
            serializer = ChoiceQuestionSerializer

        return serializer(instance).data
