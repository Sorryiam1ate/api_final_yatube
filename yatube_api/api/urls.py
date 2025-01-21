from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import (
    CommentsViewSet,
    GroupsViewSet,
    PostsViewSet,
    FollowViewSet,
)

router_v1 = DefaultRouter()
router_v1.register('posts', PostsViewSet, basename='posts')
router_v1.register('groups', GroupsViewSet, basename='groups')
router_v1.register('follow', FollowViewSet, basename='follow')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentsViewSet,
    basename='post-comments'
)


api_v1_patterns = [
    path('', include(router_v1.urls)),
    # Обновление токенов и регистрация
    # path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]


urlpatterns = [
    path('v1/', include(api_v1_patterns)),
]
