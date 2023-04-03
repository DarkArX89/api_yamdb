from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import MeUserApiView, SignUpUserView, UserViewSet, UserToken

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/users/me/', MeUserApiView.as_view()),
    path('v1/auth/signup/', SignUpUserView.as_view()),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', UserToken.as_view()),
]
