from django.forms import ValidationError
from django.test import TestCase
from .models import Form, NumericQuestion

class NumericQuestionTestCase(TestCase):
    def setUp(self):
        form = Form.objects.create(title="Test Form")
        self.numeric_question = NumericQuestion.objects.create(
            form=form,
            text="Test Numeric Question",
            is_required=True,
            question_type="numeric",
            min_value=10,
            max_value=100,
            is_decimal_allowed=False
        )

    def test_numeric_question_creation(self):
        self.assertEqual(self.numeric_question.text, "Test Numeric Question")
        self.assertEqual(self.numeric_question.is_required, True)
        self.assertEqual(self.numeric_question.question_type, "numeric")
        self.assertEqual(self.numeric_question.min_value, 10)
        self.assertEqual(self.numeric_question.max_value, 100)
        self.assertEqual(self.numeric_question.is_decimal_allowed, False)

    def test_numeric_question_min_max_validation(self):
        self.numeric_question.min_value = 100
        self.numeric_question.max_value = 50
        with self.assertRaises(ValidationError):
            self.numeric_question.clean()