from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse(viewname='users-list', request=request, format=format),
        'snippets': reverse(viewname='snippets-list', request=request, format=format),
    })


class SnippetList(
    generics.ListCreateAPIView
):
    """
    List all code snippets, or create a new snippet.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(
    generics.RetrieveUpdateDestroyAPIView
):
    """
    Retrieve, update or delete a code snippet.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class UserList(
    generics.ListAPIView
):
    """
    List all users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(
    generics.RetrieveAPIView
):
    """
    Retrieve users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetHighlight(
    generics.GenericAPIView
):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlight)
