from rest_framework import serializers
from .models import Form, ShortTextQuestion, LongTextQuestion, EmailQuestion, NumericQuestion

class FormSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Form
        fields = ['id', 'title', 'created_at', 'questions']

    def get_questions(self, obj):
        return {
            "short_text_questions": ShortTextQuestionSerializer(obj.short_text_questions.all(), many=True).data,
            "long_text_questions": LongTextQuestionSerializer(obj.long_text_questions.all(), many=True).data,
            "email_questions": EmailQuestionSerializer(obj.email_questions.all(), many=True).data,
            "numeric_questions": NumericQuestionSerializer(obj.numeric_questions.all(), many=True).data,
        }

class ShortTextQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortTextQuestion
        fields = ['id', 'form', 'text', 'is_required', 'question_type', 'max_length']

class LongTextQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongTextQuestion
        fields = ['id', 'form', 'text', 'is_required', 'question_type', 'max_length']

class EmailQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailQuestion
        fields = ['id', 'form', 'text', 'is_required', 'question_type']

class NumericQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumericQuestion
        fields = [
            'id', 'form', 'text', 'is_required', 'question_type', 
            'min_value', 'max_value', 'is_decimal_allowed'
        ]
