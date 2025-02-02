from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        def validate_username(self, value):
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError("Username already exists.")
            return value

        def validate_email(self, value):
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists.")
            return value
        




class VerifyEmailSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField()