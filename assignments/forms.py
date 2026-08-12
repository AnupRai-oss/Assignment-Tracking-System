"""
forms.py — the form students fill in to add a new assignment.

A Django Form is a Python class that DESCRIBES a form:
which fields it has, what kind of input each one needs,
and how to validate whatever the user types.
"""

from django import forms

from .models import Assignment


class AssignmentForm(forms.ModelForm):
    """
    ModelForm = a shortcut form built FROM a model.

    Django reads our Assignment model and automatically creates
    an input field for every field we list below. We do NOT have
    to write <input> HTML tags by hand — Django does it for us.
    """

    class Meta:
        # Which database model this form creates/edits.
        model = Assignment

        # Which model fields appear on the form.
        # 'status' is NOT here, so every new assignment is created
        # with the model's default status ("Pending") automatically.
        fields = [
            "title",
            "course",
            "subject_teacher",
            "description",
            "due_date",
        ]

        # widgets = small tweaks to how a field LOOKS in the browser.
        widgets = {
            # type="date" turns a plain text box into a date picker.
            "due_date": forms.DateInput(attrs={"type": "date"}),
            # Make the description box a bit shorter than the default.
            "description": forms.Textarea(attrs={"rows": 3}),
        }
