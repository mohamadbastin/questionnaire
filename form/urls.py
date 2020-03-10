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
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views

from apiv1.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/check/', UsernameValidationView.as_view()),
    path('signup/', SignupView.as_view()),
    path('connection/', IsConnected.as_view()),
    url(r'^api-token-auth/', views.obtain_auth_token),
    path('form/list/', FormListView.as_view()),
    path('form/detail/<int:formid>', FormRetrieveView.as_view()),
    # path('time/', TimeView.as_view()),
    path('form/questions/<int:form>', FormQuestionListView.as_view()),
    path('user/forms/<int:user>', CreatedFormListView.as_view()),
    path('user/created-forms/', MyCreatedFormListView.as_view()),
    path('user/answered-form/', MyAnsweredFormListView.as_view()),
    path('form/participants/<int:formid>', FormParticipantListView.as_view()),
    path('form/participant/answered-form/<int:formid>/<int:ppid>', ParticipantAnsweredFormView.as_view()),
    path('form/request/<int:formid>', SendRequestView.as_view()) ,
    path('user/profile/detail/', ProfileRetrieveView.as_view()),
    path('user/profile/<int:user>', OthersProfileRetrieveView.as_view()),
    path('user/accepted-request/<int:req>', AcceptRequestView.as_view()) ,
    path('user/rejected-request/<int:req>' , RejectRquestView.as_view()) ,
]
