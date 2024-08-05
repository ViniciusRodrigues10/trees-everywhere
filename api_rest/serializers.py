from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Account, Profile, Tree, PlantedTree
from typing import Type


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "name", "created", "active"]


class ProfileSerializer(serializers.ModelSerializer):
    user: Type[UserSerializer] = UserSerializer()

    class Meta:
        model = Profile
        fields = ["user", "about", "joined"]


class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = ["id", "name", "scientific_name"]


class PlantedTreeSerializer(serializers.ModelSerializer):
    tree = serializers.PrimaryKeyRelatedField(queryset=Tree.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = PlantedTree
        fields = ["id", "planted_at", "age", "location", "tree", "user", "account"]
