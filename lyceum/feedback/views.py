__all__ = ("feedback",)

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from feedback.forms import FeedbackForm


def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Спасибо за ваше обращение!"))
            return redirect("feedback:feedback")
    else:
        form = FeedbackForm()

    return render(request, "feedback/feedback.html", {"form": form})
