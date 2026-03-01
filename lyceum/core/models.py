from django.core.exceptions import ValidationError
import django.db.models

from core.utils import normalize_name

__all__ = [
    "BaseIsPublishedModel",
    "BaseNameModel",
    "NormalizedNameMixinModel",
]


class BaseNameModel(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=150,
        unique=True,
        verbose_name="название",
        help_text="max 150 символов",
    )

    class Meta:
        abstract = True

    def __str__(self):
        if len(self.name) > 15:
            return f"{self.name[:15]}"
        return self.name


class BaseIsPublishedModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name="опубликовано",
        help_text="опубликовано ли?",
    )

    class Meta:
        abstract = True


class NormalizedNameMixinModel(django.db.models.Model):
    normalized_name = django.db.models.CharField(
        max_length=150,
        unique=True,
        editable=False,
        verbose_name="нормализованное имя",
        help_text="нормализованное имя с проверкой на уникальность",
    )

    class Meta:
        abstract = True

    def get_normalized_name(self):
        return normalize_name(self.name)

    def validate_normalized_unique(self):
        normalized = self.get_normalized_name()

        queryset = self.__class__.objects.exclude(pk=self.pk).filter(
            normalized_name=normalized,
        )

        if queryset.exists():
            raise ValidationError(
                {
                    "name": f"{self._meta.verbose_name} с похожим именем"
                    + " уже существует",
                },
            )

    def clean(self):
        super().clean()
        self.validate_normalized_unique()

    def save(self, *args, **kwargs):
        self.normalized_name = self.get_normalized_name()
        self.full_clean()
        super().save(*args, **kwargs)
