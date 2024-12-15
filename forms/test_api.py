from django.urls import reverse


def test_create_form_valid(self):
    """
    Test creating a form with valid input.
    """
    url = reverse('form-list')
    data = {
        "title": "New Form",
        "description": "A new test form",
        "questions": [
            {
                "question_type": "short_text",
                "text": "What is your favorite color?",
                "is_required": True
            }
        ]
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Form.objects.count(), 2)
    self.assertEqual(Form.objects.last().title, "New Form")
    self.assertEqual(Form.objects.last().description, "A new test form")
    self.assertEqual(Form.objects.last().questions.count(), 1)
    self.assertEqual(Form.objects.last().questions.first().text, "What is your favorite color?")
    self.assertEqual(Form.objects.last().questions.first().is_required, True)