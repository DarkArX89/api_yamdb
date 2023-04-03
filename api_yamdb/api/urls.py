from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import MeUserApiView, SignUpUserView, UserViewSet, UserToken, TitleViewSet, CategoryViewSet, GenreViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/users/me/', MeUserApiView.as_view()),
    path('v1/auth/signup/', SignUpUserView.as_view()),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', UserToken.as_view()),
]