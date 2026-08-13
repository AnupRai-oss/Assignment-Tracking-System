"""
views.py — the "brain" of the assignments app.

A Django VIEW is just a Python function that receives a request
(what the user asked for) and returns a response (a web page).

For this page we write a plain FUNCTION-BASED VIEW — the simplest
kind of view — because we want every concept to be easy to see.
"""

from django.shortcuts import get_object_or_404, redirect, render

from rest_framework import status, viewsets
from rest_framework.response import Response

from .forms import AssignmentForm
from .models import Assignment
from .serializers import AssignmentSerializer


def assignment_list(request):
    """
    Show the "add assignment" form AND the list of assignments on ONE page.

    HTTP has two common "methods" (kinds of requests):

      * GET  -> "give me the page"   (used when you type a URL / refresh)
      * POST -> "here is form data, please save it"
                (used when you submit a <form method="post">)

    So this one function handles BOTH jobs:
      1. GET  -> build an empty form and show the page.
      2. POST -> fill the form with what the student typed, check it,
                 save it to the database, then send the browser back
                 to the page so the new assignment appears.
    """

    # ---- 1. Did the user submit the form? -------------------------
    if request.method == "POST":
        # Build a form and pour the submitted data into it.
        # Django checks every field for us (required fields,
        # valid dates, lengths, ...) when we call is_valid().
        form = AssignmentForm(request.POST)

        if form.is_valid():
            # The data passed all the checks -> save a new row.
            form.save()

            # POST/Redirect/GET pattern: after saving, tell the browser
            # "go look at the page again". This stops a page refresh
            # from accidentally saving the same assignment twice!
            return redirect("assignments:assignment_list")

        # If the form is NOT valid we fall through and re-render the
        # page. Django fills form.errors so the template can show the
        # student exactly what went wrong.

    else:
        # ---- 2. Normal page visit (GET) ----------------------------
        # A fresh, empty form, ready for the student to fill in.
        form = AssignmentForm()

    # Pull every assignment out of the database. Newest first,
    # because that ordering is set on the model's Meta class.
    assignments = Assignment.objects.all()

    # render() = "fill this template with this data and send it back".
    return render(
        request,
        "assignments/assignment_list.html",
        {
            "form": form,                 # the form (empty, or with errors)
            "assignments": assignments,   # every row in the database
        },
    )


def assignment_edit(request, pk):
    """
    Edit ONE existing assignment.

    POST -> save the changes, then go back to the list page.
    GET  -> show the list page with the modal open in "Edit" mode.
    """
    assignment = get_object_or_404(Assignment, pk=pk)

    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect("assignments:assignment_list")
    else:
        form = AssignmentForm(instance=assignment)

    return render(
        request,
        "assignments/assignment_list.html",
        {
            "form": form,
            "assignments": Assignment.objects.all(),
            "edit_pk": pk,  # tells the template to open the modal in edit mode
        },
    )


def assignment_delete(request, pk):
    """Delete ONE assignment, then go back to the list page."""
    assignment = get_object_or_404(Assignment, pk=pk)
    assignment.delete()
    return redirect("assignments:assignment_list")


# ---------------------------------------------------------------------
# Below: the existing REST API (Django REST Framework).
# It is a separate, JSON-based way to talk to the SAME data.
# The HTML page above is for humans; the API below is for apps.
# ---------------------------------------------------------------------
class AssignmentViewSet(viewsets.GenericViewSet):
    """
    The complete CRUD API for assignments, written out explicitly.

    GET    /api/assignments/          -> list all
    POST   /api/assignments/          -> create one
    GET    /api/assignments/{id}/     -> fetch one
    PUT    /api/assignments/{id}/     -> fully replace one
    PATCH  /api/assignments/{id}/     -> partially update one
    DELETE /api/assignments/{id}/     -> delete one
    """

    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    # GET /assignments/
    def list(self, request):
        """Return every assignment."""
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

    # POST /assignments/
    def create(self, request):
        """Create a new assignment."""
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT / PATCH /assignments/{id}/
    def update(self, request, pk=None):
        """Update an existing assignment. PATCH only changes the given fields."""
        assignment = self.get_object()
        partial = request.method == "PATCH"
        serializer = AssignmentSerializer(assignment, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /assignments/{id}/
    def destroy(self, request, pk=None):
        """Delete an assignment."""
        assignment = self.get_object()
        assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)