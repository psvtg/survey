"""File with application serializers."""

from rest_framework import serializers

from .models import Survey, Question


class SurveysListSerializer(serializers.ModelSerializer):
    """Serializer for surveys list."""

    class Meta:
        model = Survey
        fields = ('id', 'name', 'description', 'date_start', 'date_finish', 'questions')


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for questions"""

    class Meta:
        model = Question
        fields = ('id', 'type', 'text', 'variants')


class SurveyViewSerializer(serializers.ModelSerializer):
    """Serializer for survey."""

    questions = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Survey
        fields = ('id', 'name', 'description', 'questions')
