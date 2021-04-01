from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Survey, Question, Answer, Respondent, RespondentSurveyDone

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'date_start', 'date_finish']
    search_fields = ['name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'text']
    search_fields = ['text']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['respondent', 'question', 'answer', 'survey']


@admin.register(Respondent)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'session']


@admin.register(RespondentSurveyDone)
class RespondentSurveyDoneAdmin(admin.ModelAdmin):
    list_display = ['survey', 'respondent']
