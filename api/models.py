from django.db import models
from django.contrib.auth.models import AbstractUser


class Survey(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=False)
    date_start = models.DateField(null=False)
    date_finish = models.DateField(null=False)

    class Meta:
        verbose_name_plural = "Surveys"

    def __str__(self):
        return f'{self.id}'


class Question(models.Model):
    QUESTION_TYPES = (
        ('text', 'text'),
        ('radio', 'radio'),
        ('checkbox', 'checkbox')
    )

    type = models.CharField(max_length=256, choices=QUESTION_TYPES)
    text = models.TextField(null=False)
    surveys = models.ManyToManyField(Survey, related_name='questions')
    variants = models.CharField(max_length=256, null=True, default=None, blank=True)

    class Meta:
        verbose_name_plural = "Questions"

    def __str__(self):
        return f'{self.id}'


class Respondent(models.Model):
    session = models.CharField(max_length=256, null=False)

    def __str__(self):
        return f'{self.id}'


class Answer(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE, related_name='answers', null=False)
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='answers', null=False)
    answer = models.CharField(max_length=256, null=True)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT, related_name='answers', null=False)

    class Meta:
        verbose_name_plural = "Answers"


class RespondentSurveyDone(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE, related_name='surveys_done', null=False)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT, related_name='users_done', null=False)

    class Meta:
        verbose_name_plural = "Surveys done by Respondents"
