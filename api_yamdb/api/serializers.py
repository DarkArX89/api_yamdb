from datetime import date

from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Q

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import ConfirmationCode, User


REGEX = r'^[\w.@+-]+\Z'


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class MeUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(REGEX)]
    )
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Значение username не можеть быть "mе"'
            )
        return value

    def validate(self, data):
        if User.objects.filter(
            Q(Q(username=data.get('username'))
              & ~Q(email=data.get('email')))
            | Q(Q(email=data.get('email'))
                & ~Q(username=data.get('username')))):
            raise serializers.ValidationError(
                'Такой email или username уже существует'
            )
        return data


class UserTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.SlugRelatedField(
        queryset=ConfirmationCode.objects.all(),
        slug_field='confirmation_code')

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate_confirmation_code(self, value):
        user = get_object_or_404(User, username=self.username)
        confirmation_code = get_object_or_404(ConfirmationCode, user=user)
        if value != confirmation_code:
            raise serializers.ValidationError()
        return value

    def validate_username(self, value):
        get_object_or_404(User, username=value)
        return value


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class SlugDictRelatedField(SlugRelatedField):
    def to_representation(self, obj):
        result = {
            'name': obj.name,
            'slug': obj.slug
        }
        return result


class TitleSerializer(serializers.ModelSerializer):
    category = SlugDictRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = SlugDictRelatedField(
        queryset=Genre.objects.all(),
        many=True, slug_field='slug'
    )
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title
        read_only_fields = ('rating',)

    def validate_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError(
                'Год не может быть больше текущего!'
            )
        return value
