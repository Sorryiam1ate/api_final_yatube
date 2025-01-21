from django.contrib.auth.models import User
from posts.models import Comment, Follow, Group, Post
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class PostSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'pub_date',
            'image',
            'author',
            'group',
        )


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post']


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    def validate(self, data):
        if not data.get('following'):
            raise ValidationError(
                "Поле following не может быть пустым")

        user = self.context['request'].user
        following_user = data.get('following')

        if Follow.objects.filter(user=user, following=following_user).exists():
            raise ValidationError("Вы уже подписаны на этого автора.")

        return data

    class Meta:
        model = Follow
        fields = '__all__'
