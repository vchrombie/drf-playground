from django.contrib.auth.models import User

from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
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


class SnippetViewSet(
    viewsets.ModelViewSet
):
    """
    ViewSet which provides `list`, `create`, `retrieve`,
    'update` and `destroy` actions.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, renderers=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlight)


class UserViewSet(
    viewsets.ReadOnlyModelViewSet
):
    """
    ViewSet which provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
