from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions

from .models import Respondent, Survey, RespondentSurveyDone, Question, Answer, RespondentSurveyDone
from .serializers import SurveysListSerializer, SurveyViewSerializer
from django.core import serializers

from django.db.models.sql.datastructures import Join
from django.db.models.fields.related import ForeignObject
from django.db.models.options import Options


class RespondentActiveSurveysView(generics.ListCreateAPIView):
    serializer_class = SurveysListSerializer
    
    def get(self, request):
        if not request.session.session_key:
            request.session.save()
        session = request.session.session_key

        try:
            respondent = Respondent.objects.get(session=session)
            surveys_done_by_respondent = RespondentSurveyDone.objects.filter(respondent=respondent)
            surveys_done_by_respondent = [i.survey.id for i in surveys_done_by_respondent]
            active_surveys = Survey.objects.exclude(id__in=surveys_done_by_respondent)
        except Respondent.DoesNotExist:
            respondent = None
            active_surveys = Survey.objects.all()

        serializer = SurveysListSerializer(active_surveys, many=True)

        if not respondent:
            Respondent.objects.create(session=session)

        return Response(serializer.data)


class SurveyView(APIView):
    serializer_class = SurveyViewSerializer

    def get(self, request, id):
        try:
            survey = Survey.objects.get(id=id)
        except Survey.DoesNotExist:
            return Response(status=404)

        serializer = SurveyViewSerializer(survey)

        return Response(serializer.data)

    def post(self, request, id):
        if not request.session.session_key:
            request.session.save()
        session = request.session.session_key

        try:
            respondent = Respondent.objects.get(session=session)
            survey = Survey.objects.get(id=id)
            survey_questions_ids = [i.id for i in survey.questions.all()]
            answers = request.data
            for question, answer in answers.items():
                question = Question.objects.get(id=int(question[1:]))

                if question.id not in survey_questions_ids:
                    return Response(status=400)
                
                if question.type == 'radio' and answer not in question.variants.split(','):
                    return Response(status=400)

                elif question.type == 'checkbox':
                    respondent_answers = [a for a in answer.split(',')]
                    for a in respondent_answers:
                        if a not in question.variants.split(','):
                            return Response(status=400)
                
                answer_exists = Answer.objects.filter(respondent=respondent, question=question, survey=survey)
                if len(answer_exists):
                    return Response(status=400)
                else:
                    answer_instance = Answer.objects.create(respondent=respondent, question=question, survey=survey, answer=answer)                
                    answer_instance.save()
                    survey_questions_ids.pop(survey_questions_ids.index(question.id))

            if len(survey_questions_ids):
                return Response(status=400)

            survey_done = RespondentSurveyDone.objects.create(respondent=respondent, survey=survey)
            survey_done.save()
                
            return Response(status=200)
            
        except Exception as e:
            print(e)
            return Response(status=404)


class SurveyCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = {k.name: self.request.data.get(k.name) for k in Survey._meta.__dict__['fields'] if k.name != 'id'}
            new_survey = Survey(**data)
            new_survey.save()
        except Exception as e:
            print(e)
            return Response(status=400)

        return Response({"id": new_survey.id})


class SurveyUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id):
        try:
            data = {k.name: self.request.data.get(k.name) for k in Survey._meta.__dict__['fields'] if k.name not in ('id', 'date_start')}
            survey = Survey.objects.filter(id=id).update(**data)
        except Exception as e:
            print(e)
            return Response(status=400)

        return Response({"id": id})


class SurveyDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        try:
            survey = Survey.objects.get(id=id).delete()
        except Exception as e:
            print(e)
            return Response(status=400)

        return Response({"id": id})


class SurveyQuestionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        try:
            survey = Survey.objects.get(id=id)
            question = Question.objects.get(id=request.data.get('question_id'))
            survey_questions_ids = [i.id for i in survey.questions.all()]
            if not question.id in survey_questions_ids:
                survey.questions.add(question)
                return Response(status=200)
            else:
                return Response(status=304)
            
        except Exception as e:
            print(e)
            return Response(status=404)

    def put(self, request, id):
        try:
            survey = Survey.objects.get(id=id)
            question_to_remove = int(request.data.get('question_old_id'))
            question_to_add = int(request.data.get('question_new_id'))
            survey_questions_ids = [i.id for i in survey.questions.all()]
            if question_to_remove not in survey_questions_ids:
                return Response(status=404)
            elif question_to_add in survey_questions_ids:
                return Response(status=400)
            elif question_to_remove == question_to_add:
                return Response(status=304)
            else:
                survey.questions.remove(question_to_remove)
                survey.questions.add(question_to_add)
                return Response(status=200)
            
        except Exception as e:
            print(e)
            return Response(status=404)

    def delete(self, request, id):
        try:
            survey = Survey.objects.get(id=id)
            question = Question.objects.get(id=request.data.get('question_id'))
            survey.questions.remove(question)
            return Response(status=200)
            
        except Exception as e:
            print(e)
            return Response(status=404)


class SurveysDoneView(APIView):
    def get(self,request):
        data = dict()

        surveys_done_ids = RespondentSurveyDone.objects.filter(respondent=request.data.get('respondent_id')).values('survey')
        
        for survey_done_id in surveys_done_ids:
            survey = int(survey_done_id.get('survey'))
            survey_done_data = list()

            survey_done_answers = Answer.objects.filter(survey=survey)
            
            for q in survey_done_answers:
                survey_done_data.append({q.question.text: q.answer})

            data.update({survey: survey_done_data})

        return Response(data)