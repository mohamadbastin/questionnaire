from django.contrib import admin

# Register your models here.
from .models import *


class FormAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']


admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Operator)
admin.site.register(FormRequest)
admin.site.register(AnsweredForm)
admin.site.register(Form, FormAdmin)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(AnswerChoiceRelation)
admin.site.register(TextQuestion)
admin.site.register(RangeQuestion)
admin.site.register(ChoiceQuestion)
admin.site.register(Time)
