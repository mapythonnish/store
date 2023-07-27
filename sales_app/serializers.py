from rest_framework import serializers
from django.contrib.auth.models import User
import re



class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    # want a signup code for registering the user

    def validate_email(self, email):
        """
        Validates the given email address using a regular expression.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if bool(re.match(pattern, email)):
            return email
        return False

    def validate_password(self, password):
        """
        Validates the given password to ensure that it meets certain criteria.
        """
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        if not any(not char.isalnum() for char in password):
            return False
        return password

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        return attrs

    def create(self, validated_data):
        email = validated_data["email"]
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "This email address is already registered.")

        validated_data.pop("password2")
        return User.objects.create_user(**validated_data)
    




class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=60)

    class Meta:
        model = User
        fields = ["email", "password"]

