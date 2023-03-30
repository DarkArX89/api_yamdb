from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, filters

from django_filters.rest_framework import DjangoFilterBackend, FilterSet, AllValuesFilter

from reviews.models import Title, Category, Genre
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer


class TitleFilterSet(FilterSet):
    slug = AllValuesFilter(field_name='category__slug')
    name = AllValuesFilter(field_name='name')
    year = AllValuesFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('slug', 'name', 'year')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilterSet

    def perform_create(self, serializer):
        category_slug = self.request.data.get("category")
        category_obj = get_object_or_404(Category, slug=category_slug)
        serializer.save(category=category_obj)


class CreateListDestroyRetrieveViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateListDestroyRetrieveViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyRetrieveViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
