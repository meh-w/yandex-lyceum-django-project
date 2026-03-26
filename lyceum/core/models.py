__all__ = (
    "BaseIsPublishedModel",
    "BaseNameModel",
    "NormalizedNameMixinModel",
    "PublishedManager",
)

from django.core.exceptions import ValidationError
import django.db.models

from core.utils import generate_b_variants, normalize_name


class PublishedManager(django.db.models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


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
        return self.name[:15]


class BaseIsPublishedModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name="опубликовано",
        help_text="опубликовано ли?",
    )

    objects = django.db.models.Manager()
    published = PublishedManager()

    class Meta:
        abstract = True


class NormalizedNameMixinModel(django.db.models.Model):
    normalized_name = django.db.models.CharField(
        max_length=150,
        unique=False,
        editable=False,
        verbose_name="нормализованное имя",
        help_text="нормализованное имя",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.normalized_name = self.get_normalized_name()

        if not kwargs.get("raw", False):
            self.full_clean()

        super().save(*args, **kwargs)

    def get_normalized_name(self):
        return normalize_name(self.name)

    def clean(self):
        super().clean()
        normalized = self.get_normalized_name()

        queryset = self.__class__.objects.exclude(pk=self.pk).filter(
            normalized_name=normalized,
        )

        if queryset.exists():
            raise ValidationError(
                {
                    "name": f"{self._meta.verbose_name} с похожим именем уже"
                    + " существует",
                },
            )

        for candidate in generate_b_variants(normalized):
            if (
                self.__class__.objects.exclude(pk=self.pk)
                .filter(normalized_name=candidate)
                .exists()
            ):
                raise ValidationError(
                    {
                        "name": f"{self._meta.verbose_name} с похожим именем"
                        + " уже существует",
                    },
                )
