import re

from django.conf import settings

__all__ = ["ReverseRussianEveryTenthMiddleware"]

RUSSIAN_WORD_RE = re.compile(r"[А-Яа-яЁё]+")


class ReverseRussianEveryTenthMiddleware:
    counter = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not settings.ALLOW_REVERSE:
            return response

        self.__class__.counter += 1

        if self.__class__.counter % 10 != 0:
            return response

        text = response.content.decode(response.charset)

        def reverse_word(match: re.Match) -> str:
            return match.group(0)[::-1]

        new_text = RUSSIAN_WORD_RE.sub(reverse_word, text)

        response.content = new_text.encode(response.charset)

        return response
