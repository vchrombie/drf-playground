from django.urls import path, include

from rest_framework.routers import DefaultRouter

from snippets.views import SnippetViewSet, UserViewSet

router = DefaultRouter()

router.register(r'snippets', viewset=SnippetViewSet)
router.register(r'users', viewset=UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
