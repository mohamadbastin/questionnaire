# Create your views here.

from kavenegar import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *

dic = {"True": True, "true": True, True: True, "False": False, "false": False, False: False, None: False}

from form.settings import SMS_API_KEY


def send_verify(api_key, phone, token):
    try:
        api = KavenegarAPI(api_key)
        string = "کد تایید شما: {}  AskFill".format(token)
        params = {
            'receptor': phone,
            'message': string,
        }
        response = api.sms_send(params)
        print(response)
        Message.objects.create(to=phone, token=token, )
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


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
    allowed_methods = ["GET"]

    serializer_class = MyQuestionSerializer

    def get_queryset(self):
        f = Form.objects.get(id=self.kwargs.get('form'))
        ls = []
        for i in Question.objects.filter(form=f):
            if i.type == "text":
                ls.append(TextQuestion.objects.get(id=i.id))
            elif i.type == "range":
                ls.append(RangeQuestion.objects.get(id=i.id))
            elif i.type == "choice":
                ls.append(ChoiceQuestion.objects.get(id=i.id))
        return ls


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


class MyAnsweredFormsListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSerializer

    def get_queryset(self):
        tmp_user = self.request.user
        tmp_profile = Profile.objects.get(user=tmp_user)
        ls = []
        for i in Form.objects.filter(is_active=True, is_repeated=True):
            print(i.participant_list)
            if tmp_profile in i.participant_list.all():
                ls.append(i)
        return ls


class UserActiveFormsListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSerializer

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile.formm.filter(is_repeated=True, is_active=True)


class RemoveParticipate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChoiceSerializer

    def post(self, request, *args, **kwargs):
        pr = Profile.objects.get(user=self.request.user)
        frm = Form.objects.get(id=kwargs.get('fid'))
        frm.participant_list.remove(pr)
        frm.save()
        return Response({"msg": "ok"}, status=status.HTTP_200_OK)


class Participate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChoiceSerializer

    def post(self, request, *args, **kwargs):
        pr = Profile.objects.get(user=self.request.user)
        frm = Form.objects.get(id=kwargs.get('fid'))
        password = request.data.get('password', ' ')

        if frm.is_private:
            if frm.password == password:
                frm.participant_list.add(pr)
                frm.save()
                return Response({"msg": "ok"}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "pass wrong"}, status=status.HTTP_403_FORBIDDEN)
        else:
            frm.participant_list.add(pr)
            frm.save()
            return Response({"msg": "ok"}, status=status.HTTP_200_OK)


class RemovePart(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChoiceSerializer

    def post(self, request, *args, **kwargs):
        pr = Profile.objects.get(user=self.request.user)
        frm = Form.objects.get(id=kwargs.get('fid'))
        frm.participant_list.remove(pr)
        frm.save()


class FormParticipantListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        formid = self.kwargs.get("formid")
        return Profile.objects.filter(answered_form__form=formid).distinct()


class ParticipantAnsweredFormView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnsweredFormSerializer

    # allowed_methods = ['GET', 'POST']
    def post(self, request, *args, **kwargs):
        pass

    def get_queryset(self):
        # 2020 - 04 - 13
        date = self.request.data.get('date', None)
        formid = self.kwargs.get("formid")
        participant = self.kwargs.get("ppid")
        print(date)
        # if date:
        #     if date != 0 or date != "0":
        #         year = int(date[0, 4])
        #         month = int(date[5, 7])
        #         day = int(date[8,])
        #
        #         return AnsweredForm.objects.filter(form=formid, participant=participant, date__year=year,
        #                                            date__month=month,
        #                                            date__day=day).order_by("-date")

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


class FormCreateView(CreateAPIView):
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticated]

    # post example
    # {
    #     "name"
    #     "description"
    #     "is_private"
    #     "estimated_time"
    #     "is_repeated"
    #     "duration_days"
    #     "is_active"
    #     "times"
    # }

    def post(self, request, *args, **kwargs):
        f = Form.objects.create(author=Profile.objects.get(user=self.request.user), name=request.data.get("name"),
                                description=request.data.get("description"),
                                is_active=dic[request.data.get("is_active")],
                                is_private=dic[request.data.get("is_private")],
                                is_repeated=dic[request.data.get("is_repeated")],
                                estimated_time=int(request.data.get("estimated_time")))

        # if dic[request.data.get("is_repeated")]:
        #     f.duration_days = int(request.data.get("duration_days"))
        #     f.save()
        # else:
        f.duration_days = None
        f.save()

        if f.is_private:
            f.password = self.request.data.get('password')
            f.save()

        try:
            a = request.data.get('times')
            for i in a:
                print('f')
                Time.objects.create(form=f, hour=str(i))
        except:
            pass

        return Response({"form_id": f.pk}, status=status.HTTP_201_CREATED)


class FormUpdateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormSerializer

    def post(self, request, *args, **kwargs):
        fid = self.kwargs.get("fid")
        f = Form.objects.get(id=fid)
        f.name = request.data.get("name")
        f.description = request.data.get("description")
        f.is_active = dic[request.data.get("is_active")]
        f.is_private = dic[request.data.get("is_private")]
        f.is_repeated = dic[request.data.get("is_repeated")]
        f.estimated_time = int(request.data.get("estimated_time"))

        if dic[request.data.get("is_repeated")]:
            f.duration_days = int(request.data.get("duration_days"))
            f.save()
        else:
            f.duration_days = None
            f.save()

        f.save()

        return Response({"form_id": f.pk}, status=status.HTTP_200_OK)


class FormQuestionAddView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    # [
    #     {
    #         "type": "text"/"choice"/"range"
    #         "text"
    #         "number"
    #         "description"
    #
    #         //"text"
    #
    #         //"range"
    #         start
    #         start text
    #         end
    #         end text
    #
    #         //choice
    #         choice_type MA SA
    #         choices:[
    #              {
    #                  text
    #              }
    #         ]
    #     }
    # ]
    def post(self, request, *args, **kwargs):
        fid = self.kwargs.get("fid")
        f = Form.objects.get(id=fid)

        for i in self.request.data:
            if i["type"] == "text":
                TextQuestion.objects.create(form=f, text=i["text"], description=i["description"],
                                            number=int(i["number"]), type=i["type"])

            elif i["type"] == 'range':
                RangeQuestion.objects.create(form=f, text=i["text"], description=i["description"],
                                             number=int(i["number"]), start=1, end=10,
                                             start_text=i["start_text"], end_text=i["end_text"], type=i["type"])

            elif i["type"] == "choice":
                a = ChoiceQuestion.objects.create(form=f, choice_type=i["choice_type"], text=i["text"],
                                                  description=i["description"],
                                                  number=int(i["number"]), type=i["type"])

                for j in i["choices"]:
                    Choice.objects.create(question=a, text=j["text"])

        return Response({"msg": "created"}, status=status.HTTP_201_CREATED)


class FormAnswerCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]

    # [
    #     {
    #         question: int
    #
    #         //text
    #         text
    #
    #         //range
    #         number
    #
    #         //choice
    #         choices=[
    #             {
    #                 id
    #             }
    #         ]
    #     }
    # ]

    def post(self, request, *args, **kwargs):
        fid = self.kwargs.get("fid")
        f = Form.objects.get(id=fid)

        r = self.request.user
        p = Profile.objects.get(user=r)

        af = AnsweredForm.objects.create(form=f, participant=p)
        for i in request.data:
            q = Question.objects.get(id=int(i["question"]))
            if q.type == "text":
                Answer.objects.create(answered_form=af, question=q, text=i["text"])
            elif q.type == "range":
                Answer.objects.create(answered_form=af, question=q, number=i["number"])
            elif q.type == "choice":
                a = Answer.objects.create(answered_form=af, question=q)
                for j in i["choices"]:
                    AnswerChoiceRelation.objects.create(answer=a, choice_id=int(j["id"]))

        return Response({"msg": "submitted"}, status=status.HTTP_200_OK)


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
        tmp_profile = Profile.objects.get(user=tmp_user)
        return tmp_profile


class AcceptRequestView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get(self, request, *args, **kwargs):
        tmp_request = self.kwargs.get("req")
        tmp_request = FormRequest.objects.get(id=tmp_request)
        tmp_request.status = "ACC"
        tmp_request.save()
        return Response({"msg": "Accepted"}, status=status.HTTP_202_ACCEPTED)


class RejectRequestView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get(self, request, *args, **kwargs):
        tmp_request = self.kwargs.get("req")
        tmp_request = FormRequest.objects.get(id=tmp_request)
        tmp_request.delete()
        return Response({"msg": "Deleted"}, status=status.HTTP_200_OK)


class ChangePasswordView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        password = request.data.get("password", None)
        user.set_password(password)
        user.save()
        return Response({"msg": "password changed"}, status=status.HTTP_200_OK)


class ProfileUpdateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        tmp_user = self.request.user
        tmp_profile = Profile.objects.get(user=tmp_user)
        tmp_profile.name = request.data.get("name", None)
        tmp_profile.phone = request.data.get("phone", None)
        tmp_profile.picture = request.data.get("picture", None)
        tmp_profile.email = request.data.get("email", None)
        tmp_profile.save()
        return Response({"msg": "profile updated"}, status=status.HTTP_200_OK)


# class FormQuestionUpdateView(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#
#     # [
#     #     {
#     #         "type": "text"/"choice"/"range"
#     #         "text"
#     #         "number"
#     #         "description"
#     #
#     #         //"text"
#     #
#     #         //"range"
#     #         start
#     #         start text
#     #         end
#     #         end text
#     #
#     #         //choice
#     #         choice_type MA SA
#     #         choices:[
#     #              {
#     #                  text
#     #              }
#     #         ]
#     #     }
#     # ]
#     def post(self, request, *args, **kwargs):
#         f = self.kwargs.get("fid")
#         f = Form.objects.get(id=f)
#
#         for i in self.request.data:
#
#             if i["type"] == "text":
#                 try:
#                     t = TextQuestion.objects.get(form=f, text=i["text"])
#                     t.text = i["text"]
#                     t.description = i["description"]
#                     t.save()
#                 except Question.DoesNotExist:
#                     TextQuestion.objects.create(form=f, text=i["text"], description=i["description"],
#                                                 number=int(i["number"]), type=i["type"])
#
#             elif i["type"] == 'range':
#                 t = f.question.get(id=i["id"])
#                 t.form = f
#                 t.text = i["text"]
#                 t.description = i["description"]
#                 t.number = int(i["number"])
#                 t.start = int(i["start"])
#                 t.end = int(i["end"])
#                 t.start_text = i["start_text"]
#                 t.end_text = i["end_text"]
#                 t.type = i["type"]
#                 t.save()
#
#             elif i["type"] == "choice":
#                 t = f.question.get(id=i["id"])
#                 t.form = f
#                 t.choice_type = i["choice_type"]
#                 t.text = i["text"]
#                 t.description = i["description"]
#                 t.number = int(i["number"])
#                 t.type = i["type"]
#                 t.save()
#
#                 for j in i["choices"]:
#                     b = Choice.objects.get_or_create(id=j["id"])
#                     b.question = t
#                     b.text = j["text"]


class FormQuestionUpdateView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        f = self.kwargs.get("fid")
        f = Form.objects.get(id=f)

        dis = len(request.data)
        if dis == 0:
            return Response({"msg": "0 questions"})

        f.question.all().delete()

        for i in self.request.data:
            if i["type"] == "text":
                TextQuestion.objects.create(form=f, text=i["text"], description=i["description"],
                                            number=int(i["number"]), type=i["type"])

            elif i["type"] == 'range':
                RangeQuestion.objects.create(form=f, text=i["text"], description=i["description"],
                                             number=int(i["number"]), start=int(i["start"]), end=int(i["end"]),
                                             start_text=i["start_text"], end_text=i["end_text"], type=i["type"])

            elif i["type"] == "choice":
                a = ChoiceQuestion.objects.create(form=f, choice_type=i["choice_type"], text=i["text"],
                                                  description=i["description"],
                                                  number=int(i["number"]), type=i["type"])

                for j in i["choices"]:
                    Choice.objects.create(question=a, text=j["text"])

        return Response({"msg": "updated"}, status=status.HTTP_200_OK)


class IsFormFilledByUserView(ListAPIView):
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        prf = Profile.objects.get(user=self.request.user)
        frm = Form.objects.get(id=kwargs.get('fid'))

        try:
            a = AnsweredForm.objects.get(form=frm, participant=prf)
            return Response({"is_filled": True}, status=status.HTTP_200_OK)
        except AnsweredForm.DoesNotExist:
            return Response({"is_filled": False}, status=status.HTTP_404_NOT_FOUND)


class MyAnsweredFormView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnsweredFormSerializer

    def get_queryset(self):
        formid = self.kwargs.get("formid")
        participant = Profile.objects.get(user=self.request.user)

        return AnsweredForm.objects.filter(form=formid, participant=participant).order_by("-date")


class Register(CreateAPIView):
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        phone = self.request.data.get("phone")
        name = self.request.data.get('name')
        try:
            a = User.objects.get(username=phone)
            # a.set_password("1111")
            # a.save()

            # password = randint(1000, 9999)
            password = '1111'
            a.set_password(password)
            a.save()
            send_verify(SMS_API_KEY, phone, str(password))
            # message = Message(token=password, to=phone)

            # operator = Operator.objects.get(name="sahar")
            # operator.send_message(message)

            p = Profile.objects.get(user=a)
            if p.name == None or p.name == '':
                p.name = name
                p.save()
        except User.DoesNotExist:
            a = User.objects.create_user(username=phone)
            # password = randint(1000, 9999)
            password = '1111'
            a.set_password(password)
            a.save()

            send_verify(SMS_API_KEY, phone, str(password))
            # message = Message(token=password, to=phone)
            #
            # operator = Operator.objects.get(name="sahar")
            # operator.send_message(message)
            b = Profile.objects.create(user=a, name=name)

        return Response({"msg": "ok"}, status=status.HTTP_200_OK)


class ReportByQuestion(ListAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        ppid = self.request.data.get('ppid')
        date = self.request.data.get('date')
        qid = self.kwargs.get('qid')
        a = Answer.objects.filter(question=Question.objects.get(pk=qid))
        if ppid != 0:
            a.filter(answered_form__participant=Profile.objects.get(pk=ppid))
        if date != 0:
            print(date)

        return a
