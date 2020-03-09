from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(Request)
admin.site.register(AnsweredForm)
admin.site.register(Form)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(AnswerChoiceRelation)
admin.site.register(TextQuestion)
admin.site.register(RangeQuestion)
admin.site.register(ChoiceQuestion)
admin.site.register(Time)

