from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer, UserAuthSerializer, ConfirmUserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmationCode
from rest_framework.views import APIView
import random
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'key': token.key})
        return Response({'error': 'user credentials are wrong!'}, status=status.HTTP_401_UNAUTHORIZED)


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = User.objects.create_user(email=email, password=password, is_active=False)

        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        ConfirmationCode.objects.create(user=user, code=code)

        print(f'Код подтверждения для пользователя {email}: {code}')  # Для отладки

        return Response(
            {'user_id': user.id, 'detail': 'Пользователь создан. Проверьте код подтверждения.'},
            status=status.HTTP_201_CREATED
        )


class ConfirmUserAPIView(APIView):
    def post(self, request):
        serializer = ConfirmUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Пользователь подтвержден и активирован"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = authenticate(username=username, password=password)
    if user:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'user credentials are wrong!'})

@api_view(['POST'])
def registraion_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(username=username, password=password, is_active=False)

    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    ConfirmationCode.objects.create(user=user, code=code)

    print(f'Код подтверждения для пользователя {username}: {code}')  # Для отладки

    return Response(
        data={'user_id': user.id, 'detail': 'Пользователь создан. Проверьте код подтверждения.'},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def confirm_user_api_view(request):
    serializer = ConfirmUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Пользователь подтвержден и активирован"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)