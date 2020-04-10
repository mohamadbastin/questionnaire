"""form URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views

from apiv1.views import *
from form import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/check/', UsernameValidationView.as_view()),
    path('signup/', SignupView.as_view()),
    path('connection/', IsConnected.as_view()),
    url(r'^login/', views.obtain_auth_token),
    path('form/list/', FormListView.as_view()),
    path('form/detail/<int:formid>', FormRetrieveView.as_view()),
    # path('time/', TimeView.as_view()),
    path('form/questions/<int:form>', FormQuestionListView.as_view()),
    path('user/forms/<int:user>', CreatedFormListView.as_view()),
    path('user/created-forms/', MyCreatedFormListView.as_view()),
    path('user/answered-form/', MyAnsweredFormsListView.as_view()),
    path('form/participants/<int:formid>', FormParticipantListView.as_view()),
    path('form/participant/answered-form/<int:formid>/<int:ppid>', ParticipantAnsweredFormView.as_view()),
    # path('request/<int:formid>', SendRequestView.as_view()),
    path('form/create/', FormCreateView.as_view()),
    path('form/update/<int:fid>', FormUpdateView.as_view()),
    path('form/question/create/<int:fid>', FormQuestionAddView.as_view()),
    path('form/answer/<int:fid>', FormAnswerCreate.as_view()),
    path('form/request/<int:formid>', SendRequestView.as_view()),
    path('profile/', ProfileRetrieveView.as_view()),
    path('user/profile/<int:user>', OthersProfileRetrieveView.as_view()),
    path('user/accepted-request/<int:req>', AcceptRequestView.as_view()),
    path('user/rejected-request/<int:req>', RejectRequestView.as_view()),
    path('user/change-password/', ChangePasswordView.as_view()),
    path('user/profile/update/', ProfileUpdateView.as_view()),
    path('form/questions/update/<int:fid>', FormQuestionUpdateView.as_view()),
    path('connection', IsConnected.as_view()),
    path('form/is-filled/<int:fid>', IsFormFilledByUserView.as_view()),
    path('form/my-answer/<int:formid>', MyAnsweredFormView.as_view()),
    path('register/', Register.as_view()),
    path('participate/', Participate.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
