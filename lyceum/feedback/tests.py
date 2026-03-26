__all__ = ("FeedbackFormTest",)

from django.test import TestCase
from django.urls import reverse

from feedback.forms import FeedbackForm


class FeedbackFormTest(TestCase):
    def test_form_in_context(self):
        response = self.client.get(reverse("feedback:feedback"))
        self.assertIn("form", response.context)

    def test_form_labels_and_help_text(self):
        form = FeedbackForm()
        self.assertEqual(
            form.fields["mail"].help_text,
            "На этот адрес будет отправлен ответ",
        )
        self.assertEqual(form.fields["name"].label, "Имя")
        self.assertEqual(form.fields["mail"].label, "Почта")
        self.assertEqual(form.fields["text"].label, "Сообщение")

    def test_form_submit_redirect(self):
        data = {
            "name": "Test User",
            "mail": "test@example.com",
            "text": "Test message",
        }
        response = self.client.post(reverse("feedback:feedback"), data)
        self.assertRedirects(response, reverse("feedback:feedback"))
