"""
web_urls.py — URLs for the human-facing web page.

(Beside this file, `urls.py` keeps the JSON API routes.
We split them into two files so the simple HTML page and the
REST API each stay easy to understand on their own.)
"""

from django.urls import path

from . import views

# Namespace for this URL file. It lets templates say
# {% url "assignments:assignment_list" %} instead of
# hard-coding "/" inside every template.
app_name = "assignments"

urlpatterns = [
    # An empty path ("") means "the root of this URL include".
    # The view `assignment_list` handles both GET and POST.
    path("", views.assignment_list, name="assignment_list"),
]