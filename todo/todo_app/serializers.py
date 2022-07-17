from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from passlib.hash import pbkdf2_sha256
from .models import ToDoUser

class UserSignUpSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = ToDoUser.objects.create(
            name = validated_data.get('name'),
            email = validated_data.get('email'),
            password = pbkdf2_sha256.hash(validated_data.get('password')),
        )
        return user
    
    class Meta:
        model = ToDoUser
        fields = '__all__'

class UserLoginInSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = ToDoUser
        fields = ['email', 'password']