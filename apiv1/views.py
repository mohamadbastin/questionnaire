from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.authtoken.models import Token


class IsConnected(ListAPIView):
    def get(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


class UsernameValidationView(CreateAPIView):
    serializer_class = ProfileSerializer
    allowed_methods = ["POST"]

    def post(self, request, *args, **kwargs):
        temp = request.data.get("username", None)
        if not temp:
            return Response({"msg": "no username"}, status=status.HTTP_400_BAD_REQUEST)

        q = User.objects.filter(username=temp)
        if q:
            return Response({"valid": "false"}, status=status.HTTP_409_CONFLICT)
        return Response({"valid": "true"}, status=status.HTTP_200_OK)


class SignupView(CreateAPIView):
    serializer_class = ProfileSerializer
    allowed_methods = ["POST"]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        name = request.data.get("name", None)
        phone = request.data.get("phone", None)
        picture = request.data.get("picture", None)
        email = request.data.get("email", None)

        if not username or not password or not name or not phone:
            return Response({"msg": "missing arguments"}, status=status.HTTP_400_BAD_REQUEST)

        tmp_user = User.objects.create_user(username=username)
        tmp_user.set_password(password)
        tmp_user.save()

        Token.objects.create(user=tmp_user)

        Profile.objects.create(user=tmp_user, name=name, phone=phone, picture=picture, email=email)

        return Response({"msg": "User Created"}, status=status.HTTP_201_CREATED)


class FormListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSerializer
    queryset = Form.objects.filter(is_active=True).order_by('-created')


class FormRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSerializer
    lookup_url_kwarg = "formid"
    queryset = Form.objects.all()


# class TimeView(ListAPIView):
#     serializer_class = TimeSerializer
#     queryset = Time.objects.all()
#

class FormQuestionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by('number')
    lookup_url_kwarg = "form"
    lookup_field = 'form'


class CreatedFormListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSerializer
    lookup_field = "author"
    lookup_url_kwarg = "user"
    queryset = Form.objects.all().order_by('-created')


class MyCreatedFormListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSerializer

    def get_queryset(self):
        tmp_user = self.request.user
        tmp_profile = Profile.objects.get(user=tmp_user)
        return Form.objects.filter(author=tmp_profile).order_by('-created')


class MyAnsweredFormListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSerializer

    def get_queryset(self):
        tmp_user = self.request.user
        tmp_profile = Profile.objects.get(user=tmp_user)
        return Form.objects.filter(answered_form__participant=tmp_profile)


class FormParticipantListView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        formid = self.kwargs.get("formid")
        return Profile.objects.filter(answered_form__form=formid)


class ParticipantAnsweredFormView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = AnsweredFormSerializer

    def get_queryset(self):
        formid = self.kwargs.get("formid")
        participant = self.kwargs.get("ppid")

        return AnsweredForm.objects.filter(form=formid, participant=participant).order_by("-date")


class SendRequestView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        formid = self.kwargs.get("formid")
        form = Form.objects.get(id=formid)
        sender = self.request.user
        sender = Profile.objects.get(user=sender)
        FormRequest.objects.create(sender=sender, form=form)

        return Response({"msg": "requested"}, status=status.HTTP_201_CREATED)


class ProfileRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        tmp_user = self.request.user
        tmp_profile = Profile.objects.get(user=tmp_user)
        return tmp_profile


class OthersProfileRetrieveView(RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        tmp_user = self.kwargs.get("user")
        tmp_profile = Profile.objects.get(user = tmp_user)
        return tmp_profile



class AcceptRequestView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get(self, request, *args, **kwargs):
        tmp_request = self.kwargs.get("req")
        tmp_request = FormRequest.objects.get(id = tmp_request)
        tmp_request.status = "ACC"
        tmp_request.save()
        return Response({"msg":"Accepted" } , status = status.HTTP_202_ACCEPTED)


class RejectRquestView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get(self, request, *args, **kwargs):
        tmp_request = self.kwargs.get("req")
        tmp_request = FormRequest.objects.get(id=tmp_request)
        tmp_request.delete()
        return Response({"msg":"Deleted"} , status= status.HTTP_200_OK)
