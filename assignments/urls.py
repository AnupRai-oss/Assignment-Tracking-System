

 

from django.urls import path

from .views import AssignmentViewSet

urlpatterns = [
    # GET  /api/assignments/          -> list all
    # POST /api/assignments/          -> create one
    path("", AssignmentViewSet.as_view({"get": "list", "post": "create"})),
]