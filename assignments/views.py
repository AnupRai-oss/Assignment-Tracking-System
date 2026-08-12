from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Assignment
from .serializers import AssignmentSerializer


# Create your views here.
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
    