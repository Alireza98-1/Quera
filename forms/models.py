from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ValidationError
from .choices import QuestionTypeChoices

class Form(models.Model):
    title = models.CharField(max_length=155, verbose_name="Form Title")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self) -> str:
        return self.title

class Question(models.Model):
    form = models.ForeignKey(Form, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=300, verbose_name="Question Text")
    is_required = models.BooleanField(default=False, verbose_name="Is Required")
    question_type = models.CharField(
        max_length=20, choices=QuestionTypeChoices.choices, verbose_name="Type"
        )
    
    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.text} ({self.get_question_type_display()})"

class ShortTextQuestion(Question):
    max_length = models.PositiveIntegerField(
        validators=[MaxValueValidator(250)], verbose_name="Max Length"
    )

class LongTextQuestion(Question):
    max_length = models.PositiveIntegerField(
        validators=[MaxValueValidator(5000)], verbose_name="Max Length"
    )

class EmailQuestion(Question):
    pass

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .choices import QuestionTypeChoices


class Form(models.Model):
    title = models.CharField(max_length=155, verbose_name="Form Title")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    text = models.CharField(max_length=300, verbose_name="Question Text")
    is_required = models.BooleanField(default=False, verbose_name="Is Required")
    question_type = models.CharField(
        max_length=20, choices=QuestionTypeChoices.choices, verbose_name="Type"
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.text} ({self.get_question_type_display()})"


class ShortTextQuestion(Question):
    max_length = models.PositiveIntegerField(
        validators=[MaxValueValidator(250)], verbose_name="Max Length"
    )

    class Meta:
        default_related_name = "short_text_questions"


class LongTextQuestion(Question):
    max_length = models.PositiveIntegerField(
        validators=[MaxValueValidator(5000)], verbose_name="Max Length"
    )

    class Meta:
        default_related_name = "long_text_questions"


class EmailQuestion(Question):
    pass

    class Meta:
        default_related_name = "email_questions"


class NumericQuestion(Question):
    min_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0)], verbose_name="Min Value"
    )
    max_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0)], verbose_name="Max Value"
    )
    is_decimal_allowed = models.BooleanField(default=False, verbose_name="Allow Decimals")

    def clean(self):
        if self.min_value is not None and self.max_value is not None and self.min_value > self.max_value:
            raise ValidationError("Minimum value cannot be greater than maximum value.")
        super().clean()

    class Meta:
        default_related_name = "numeric_questions"

