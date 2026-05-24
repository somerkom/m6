from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import ConfirmationCode, CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    birthdate = serializers.DateField(required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'phone', 'birthdate')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            emil = validated_data['email'],
            username = validated_data['username'],
            password = validated_data['password'],
            phone = validated_data.get('phone'),
            birthdate = validated_data.get('birthdate')
        )
        return user

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
        except:
            return email
        raise ValidationError('User already exists!')


class ConfirmUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data['email']
        code = data['code']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        try:
            confirmation = ConfirmationCode.objects.get(user=user)
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError("Код подтверждения не найден")

        if confirmation.code != code:
            raise serializers.ValidationError("Неверный код")

        data['user'] = user
        return data

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.is_active = True
        user.save()
        user.confirmation_code.delete()  # удаляем код
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['birthdate'] = str(user.birthdate)
        return token