__all__ = ("Feedback",)

from django.db import models


class Feedback(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    text = models.TextField(verbose_name="Текстовое поле")
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания",
    )
    mail = models.EmailField(verbose_name="Почта")

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.name} - {self.created_on}"
