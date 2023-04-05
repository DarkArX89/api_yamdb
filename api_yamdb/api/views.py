import random
import string

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend, FilterSet, AllValuesFilter

from rest_framework import generics, permissions, status, viewsets, mixins, filters
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Title, Category, Genre, Review
from users.models import ConfirmationCode, User
from .permissions import AdminOrReadOnly, AdministratorOrReadOnly, AuthorOrReadOnly
from .serializers import (
    UserSerializer, UserSignUpSerializer, UserTokenSerializer, 
    TitleSerializer, CategorySerializer, GenreSerializer,
    CommentSerializer, ReviewSerializer
)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorOrReadOnly]
    

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username')
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'username'
    lookup_url_kwarg = 'username'


class MeUserApiView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class SignUpUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            confirmation_code = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=6)
            )
            code = ConfirmationCode.objects.create(
                user=user, confirmation_code=confirmation_code
            )
            send_mail(
                subject='Confirmation_code',
                message=str(code.confirmation_code),
                from_email=get_current_site(request).domain,
                recipient_list=[serializer.data['email']],
                fail_silently=False,
            )
            output_serializer = self.serializer_class(user)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserToken(TokenObtainPairView):
    serializer_class = UserTokenSerializer
    permission_classes = (permissions.AllowAny,)


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
    permission_classes = (AdministratorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet

    # def perform_create(self, serializer):
    #     category_slug = self.request.data.get("category")
    #     category_obj = get_object_or_404(Category, slug=category_slug)
    #     serializer.save(category=category_obj)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (AdministratorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (AdministratorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
