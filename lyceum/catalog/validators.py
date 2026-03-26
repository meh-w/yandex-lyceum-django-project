__all__ = "ValidateMustContain"

import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.html import strip_tags


@deconstructible
class ValidateMustContain:
    def __init__(self, *words):
        self.words = [word.lower() for word in words]

    def __call__(self, value):
        text = strip_tags(value)

        text = text.lower()

        cleaned_value = re.sub(r"[^\w\s]", " ", text)

        words = cleaned_value.split()

        if not any(word in words for word in self.words):
            raise ValidationError(
                f"Текст должен содержать одно из: {', '.join(self.words)}",
            )
