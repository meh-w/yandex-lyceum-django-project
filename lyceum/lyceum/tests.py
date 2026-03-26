__all__ = (
    "ReverseMiddlewareEnabledTests",
    "ReverseMiddlewareDisabledTests",
    "ReverseMiddlewareDefaultTests",
)

import django.test
from django.urls import reverse

from lyceum.middleware import (
    ReverseRussianEveryTenthMiddleware,
    RUSSIAN_WORD_RE,
)


@django.test.override_settings(ALLOW_REVERSE=True)
class ReverseMiddlewareEnabledTests(django.test.TestCase):
    def setUp(self):
        ReverseRussianEveryTenthMiddleware.counter = 0

    def test_reverse_is_enabled(self):
        url = reverse("homepage:coffee")
        for _ in range(1, 10):
            response = self.client.get(url)
            self.assertEqual(response.content.decode("utf-8"), "Я чайник")

        response = self.client.get(url)
        self.assertEqual(response.content.decode("utf-8"), "Я кинйач")

    def test_20th_response_also_reversed(self):
        ReverseRussianEveryTenthMiddleware.counter = 0

        url = reverse("homepage:coffee")
        for _ in range(10):
            response = self.client.get(url)

        self.assertEqual(response.content.decode("utf-8"), "Я кинйач")

        for _ in range(9):
            response = self.client.get(url)
            self.assertEqual(response.content.decode("utf-8"), "Я чайник")

        response = self.client.get(url)
        self.assertEqual(response.content.decode("utf-8"), "Я кинйач")


@django.test.override_settings(ALLOW_REVERSE=False)
class ReverseMiddlewareDisabledTests(django.test.TestCase):
    def setUp(self):
        ReverseRussianEveryTenthMiddleware.counter = 0

    def test_reverse_is_disabled(self):
        url = reverse("homepage:coffee")
        for _ in range(1, 10 + 1):
            response = self.client.get(url)
            self.assertEqual(response.content.decode("utf-8"), "Я чайник")


class ReverseMiddlewareDefaultTests(django.test.TestCase):
    def setUp(self):
        ReverseRussianEveryTenthMiddleware.counter = 0

    def test_default_behavior(self):
        url = reverse("homepage:coffee")
        for _ in range(9):
            response = self.client.get(url)
            self.assertEqual(response.content.decode("utf-8"), "Я чайник")

        response = self.client.get(url)
        self.assertEqual(response.content.decode("utf-8"), "Я кинйач")


class ReverseWordFunctionalityTests(django.test.TestCase):
    def setUp(self):
        self.middleware = ReverseRussianEveryTenthMiddleware
        self.word_re = RUSSIAN_WORD_RE

    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_russian_words_only_reversed(self):
        def reverse_word(match):
            return match.group(0)[::-1]

        test_cases = [
            (
                "На Djangoджанго (лучшие) 24чайника чайника!",
                "аН Djangoджанго (еишчул) 24чайника акинйач!",
            ),
            (
                "Привет мир! Hello world! 123тест",
                "тевирП рим! Hello world! 123тест",
            ),
            ("Ёжик и ёлка", "кижЁ и аклё"),
            ("красно-белый сине-зеленый", "онсарк-йылеб енис-йынелез"),
            ("\"слово\" (тест) 'привет'", "\"оволс\" (тсет) 'тевирп'"),
            ("тест123тест 123тест тест123", "тест123тест 123тест тест123"),
            (
                "Djangoтест тестDjango тестDjangoтест",
                "Djangoтест тестDjango тестDjangoтест",
            ),
            ("ПрИвЕт МиР", "тЕвИрП РиМ"),
            ("... !!! ???", "... !!! ???"),
            ("", ""),
            ("Hello123 world456", "Hello123 world456"),
            ("привет, мир! как? дела:", "тевирп, рим! как? алед:"),
            ("быстро бежит лиса", "ортсыб тижеб асил"),
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.word_re.sub(reverse_word, input_text)
                self.assertEqual(result, expected)
