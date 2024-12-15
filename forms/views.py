from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Form, ShortTextQuestion, LongTextQuestion, EmailQuestion, NumericQuestion
from .serializers import (
    FormSerializer,
    ShortTextQuestionSerializer,
    LongTextQuestionSerializer,
    EmailQuestionSerializer,
    NumericQuestionSerializer,
)

class FormViewSet(ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def create(self, request, *args, **kwargs):
        form_serializer = self.get_serializer(data=request.data)
        form_serializer.is_valid(raise_exception=True)
        form = form_serializer.save()

        questions_data = request.data.get("questions", [])
        self._process_questions(questions_data, form)

        return Response(form_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        form_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        form_serializer.is_valid(raise_exception=True)
        form = form_serializer.save()

        questions_data = request.data.get("questions", [])
        self._process_questions(questions_data, form, update=True)

        return Response(form_serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        form = self.get_object()
        questions = []
        questions.extend(form.short_text_questions.all())
        questions.extend(form.long_text_questions.all())
        questions.extend(form.email_questions.all())
        questions.extend(form.numeric_questions.all())
        
        serialized_questions = []
        for question in questions:
            if isinstance(question, ShortTextQuestion):
                serializer = ShortTextQuestionSerializer(question)
            elif isinstance(question, LongTextQuestion):
                serializer = LongTextQuestionSerializer(question)
            elif isinstance(question, EmailQuestion):
                serializer = EmailQuestionSerializer(question)
            elif isinstance(question, NumericQuestion):
                serializer = NumericQuestionSerializer(question)
            serialized_questions.append(serializer.data)
        
        return Response(serialized_questions)

    @action(detail=True, methods=['post'])
    def add_question(self, request, pk=None):
        form = self.get_object()
        question_data = request.data
        question_data['form'] = form.id
        
        serializer_class = self._get_serializer_class(question_data.get('question_type'))
        if not serializer_class:
            return Response(
                {"error": f"Unsupported question type: {question_data.get('question_type')}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = serializer_class(data=question_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put', 'patch'])
    def update_question(self, request, pk=None):
        form = self.get_object()
        question_id = request.data.get('id')
        question_type = request.data.get('question_type')
        
        if not question_id or not question_type:
            return Response(
                {"error": "Both 'id' and 'question_type' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        question = self._get_question_instance(form, question_type, question_id)
        if not question:
            return Response(
                {"error": f"Question with ID {question_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer_class = self._get_serializer_class(question_type)
        serializer = serializer_class(question, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_question(self, request, pk=None):
        form = self.get_object()
        question_id = request.data.get('id')
        question_type = request.data.get('question_type')
        
        if not question_id or not question_type:
            return Response(
                {"error": "Both 'id' and 'question_type' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        question = self._get_question_instance(form, question_type, question_id)
        if not question:
            return Response(
                {"error": f"Question with ID {question_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _process_questions(self, questions_data, form, update=False):
        existing_questions = {
            "short_text": set(form.short_text_questions.values_list('id', flat=True)),
            "long_text": set(form.long_text_questions.values_list('id', flat=True)),
            "email": set(form.email_questions.values_list('id', flat=True)),
            "numeric": set(form.numeric_questions.values_list('id', flat=True)),
        }

        for question_data in questions_data:
            question_type = question_data.get("question_type")
            serializer_class = self._get_serializer_class(question_type)
            if not serializer_class:
                raise ValueError(f"Unsupported question type: {question_type}")

            question_id = question_data.get("id")
            if update and question_id:
                question = self._get_question_instance(form, question_type, question_id)
                if not question:
                    raise ValueError(f"Question with ID {question_id} not found.")
                serializer = serializer_class(question, data=question_data, partial=True)
                existing_questions[question_type].discard(question_id)
            else:
                question_data["form"] = form.id
                serializer = serializer_class(data=question_data)

            serializer.is_valid(raise_exception=True)
            serializer.save()

        if update:
            for question_type, ids_to_remove in existing_questions.items():
                self._get_question_model(question_type).objects.filter(id__in=ids_to_remove).delete()

    def _get_serializer_class(self, question_type):
        serializers_map = {
            "short_text": ShortTextQuestionSerializer,
            "long_text": LongTextQuestionSerializer,
            "email": EmailQuestionSerializer,
            "numeric": NumericQuestionSerializer,
        }
        return serializers_map.get(question_type)

    def _get_question_model(self, question_type):
        models_map = {
            "short_text": ShortTextQuestion,
            "long_text": LongTextQuestion,
            "email": EmailQuestion,
            "numeric": NumericQuestion,
        }
        return models_map.get(question_type)

    def _get_question_instance(self, form, question_type, question_id):
        model = self._get_question_model(question_type)
        return get_object_or_404(model, form=form, id=question_id)