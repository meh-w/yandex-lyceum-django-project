__all__ = ("FeedbackForm",)

from datetime import datetime
from pathlib import Path

from django import forms
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "mail", "text"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Ваше имя")}
            ),
            "mail": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "example@mail.com",
                }
            ),
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": _("Ваше сообщение..."),
                }
            ),
        }
        labels = {
            "name": _("Имя"),
            "mail": _("Почта"),
            "text": _("Сообщение"),
        }
        help_texts = {
            "mail": _("На этот адрес будет отправлен ответ"),
        }

    def _save_email_to_file(self, subject, message, recipient):
        """Сохраняет письмо в папку send_mail/"""
        send_mail_dir = Path(settings.BASE_DIR) / "send_mail"
        send_mail_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{timestamp}_{recipient.replace('@', '_at_')}.txt"
        filepath = send_mail_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Subject: {subject}\n")
            f.write(f"From: {settings.DJANGO_MAIL}\n")
            f.write(f"To: {recipient}\n")
            f.write(f"Date: {datetime.now().isoformat()}\n\n")
            f.write(message)

    def save(self, commit=True):
        instance = super().save(commit=commit)

        message_to_user = (
            f"{_('Здравствуйте')}, {instance.name}!\n\n"
            f"{_('Спасибо за ваше обращение. Мы получили ваше сообщение:')}\n"
            f'"{instance.text}"\n\n'
            f"{_('Наш специалист свяжется с вами в ближайшее время.')}\n\n"
            f"{_('С уважением')},\n"
            f"{_('Команда сайта')}"
        )

        self._save_email_to_file(
            subject=_("Ваше обращение получено"),
            message=message_to_user,
            recipient=instance.mail,
        )

        send_mail(
            subject=_("Ваше обращение получено"),
            message=message_to_user,
            from_email=settings.DJANGO_MAIL,
            recipient_list=[instance.mail],
            fail_silently=False,
        )

        return instance
