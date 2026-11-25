from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Project


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css)


class ProjectForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "client_name", "budget", "status", "deadline", "note"]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "note": forms.Textarea(attrs={"rows": 4}),
        }


class SignUpForm(BootstrapMixin, UserCreationForm):
    pass
