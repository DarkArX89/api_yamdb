import random
import string

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

from rest_framework import generics, permissions, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import ConfirmationCode, User
from .permissions import AdminOrReadOnly
from .serializers import (
    UserSerializer, UserSignUpSerializer, UserTokenSerializer
)


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
