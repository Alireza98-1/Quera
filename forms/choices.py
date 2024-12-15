from django.db.models import TextChoices

class QuestionTypeChoices(TextChoices):
    SHORT_TEXT = 'short_text', 'Short Text'
    LONG_TEXT = 'long_text', 'Long Text'
    EMAIL = 'email', 'Email'
    NUMERIC = 'numeric', 'Numeric'