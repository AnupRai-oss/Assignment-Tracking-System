from django.urls import path

from .views import AssignmentViewSet

urlpatterns = [
    # GET  /api/assignments/          -> list all
    # POST /api/assignments/          -> create one
    path("", AssignmentViewSet.as_view({"get": "list", "post": "create"})),
    # PUT / PATCH /api/assignments/{id}/   -> update one
    # DELETE     /api/assignments/{id}/   -> delete one
    path(
        "<int:pk>/",
        AssignmentViewSet.as_view({"put": "update", "patch": "update", "delete": "destroy"}),
    ),
]