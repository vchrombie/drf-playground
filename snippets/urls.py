from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views

urlpatterns = [
    path('snippets/',
         views.SnippetList.as_view(),
         name='snippets-list'),
    path('snippet/<int:pk>/',
         views.SnippetDetail.as_view(),
         name='snippet-detail'),
    path('users/',
         views.UserList.as_view(),
         name='users-list'),
    path('user/<int:pk>/',
         views.UserDetail.as_view(),
         name='user-detail'),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
