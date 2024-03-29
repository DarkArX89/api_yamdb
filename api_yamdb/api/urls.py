from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (MeUserApiView, UserViewSet, UserToken,
                       TitleViewSet, CategoryViewSet, GenreViewSet,
                       CommentViewSet, ReviewViewSet, SignUpUserView)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')

auth_patterns = [
    path('auth/signup/', SignUpUserView.as_view()),
    path('auth/token/', UserToken.as_view()),
]

urlpatterns = [
    path('v1/users/me/', MeUserApiView.as_view()),
    path('v1/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
