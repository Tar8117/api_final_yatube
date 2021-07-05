from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    text = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    # post = serializers.SlugRelatedField(read_only=True, slug_field='id')
    # ничего не изменилось насколько я понял, в мета снизу и так указал
    # что post - рид онли

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError('Нельзя подписаться на себя')
        return data

    class Meta:
        model = Follow
        fields = '__all__'
        # только чтение для поля юзер указал здесь, потому что на уровне поля
        # если указываю, то все тесты фейлятся с ошибкой:
        # AssertionError: Relational fields should not provide a
        # `queryset` argument, when setting read_only=`True`.
        read_only_fields = ('user',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=['user', 'following'],
                message='Нельзя подписаться, если уже подписан'
            )
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        # read_only_fields = ('id',) не нужно объявлять явно, потому что,
        # фреймворк это сам поймет, за счет того, что id это первичный ключ))
