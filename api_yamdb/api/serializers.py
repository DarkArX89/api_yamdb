from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Category, Genre, GenreTitle


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
            "name": obj.name,
            "slug": obj.slug
        }
        return result

class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = SlugDictRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title

    def create(self, validated_data):
        genres = self.initial_data.get('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = get_object_or_404(Genre, slug=genre)
            GenreTitle.objects.create(
                genre_id=current_genre, title_id=title
            )
        return title 
