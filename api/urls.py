from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    path('surveys/', views.RespondentActiveSurveysView.as_view()),
    path('surveys/<int:id>/', views.SurveyView.as_view()),
    path('surveys/create/', views.SurveyCreateView.as_view()),
    path('surveys/<int:id>/update/', views.SurveyUpdateView.as_view()),
    path('surveys/<int:id>/delete/', views.SurveyDeleteView.as_view()),
    path('surveys/<int:id>/questions/', views.SurveyQuestionView.as_view()),
    path('surveys/done/', views.SurveysDoneView.as_view()),
]
