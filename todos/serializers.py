from rest_framework import serializers
from .models import Todo, User

class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'Title', 'Description', 'Date', 'Completed')


# users serializers
# class UserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(max_length=150, required=True)
#     email = serializers.EmailField(max_length=254, required=True)
#     first_name = serializers.CharField(max_length=150, required=True)
#     last_name = serializers.CharField(max_length=150, required=True)
#     password = serializers.CharField(max_length=128, write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name'
                  )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user