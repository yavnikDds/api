from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password, check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fullname', 'email', 'mobile_number', 'referral_code', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(
            fullname=validated_data['fullname'],
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
            referral_code=validated_data.get('referral_code', None),
            password=make_password(validated_data['password'])  # Hash the password
        )
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        try:
            user = User.objects.get(email=email)
            if not check_password(password, user.password):
                raise serializers.ValidationError({"password":"Incorrect PassWord."})
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this email does not exist"})
        return{"user":user}
