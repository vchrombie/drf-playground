from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers

from snippets.views import SnippetViewSet, UserViewSet, api_root

snippets_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight',
},
    renderer_classes=[renderers.StaticHTMLRenderer]
)

users_list = UserViewSet.as_view({
    'get': 'list',
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',
})


urlpatterns = [
    path('', api_root, name='api-root'),
    path('snippets/', snippets_list, name='snippets-list'),
    path('snippet/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippet/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    path('users/', users_list, name='users-list'),
    path('user/<int:pk>/', user_detail, name='user-detail'),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
