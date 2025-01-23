from django.shortcuts import get_object_or_404
from rest_framework import (
    filters,
    mixins,
    viewsets
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from api.permissions import AuthorOrReadOnly
from api.serializers import (
    CommentsSerializer,
    FollowSerializer,
    GroupsSerializer,
    PostSerializer
)
from posts.models import Group, Post


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AuthorOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AuthorOrReadOnly,
    )

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(post=post, author=self.request.user)


class FollowViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = (r'^following__username',)

    def get_queryset(self):
        return self.request.user.follows.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer
