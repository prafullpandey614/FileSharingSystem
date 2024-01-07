
from rest_framework import serializers
from .models import OperationUser, ClientUser, FileSystem
from django.contrib.auth.models import User

class OperationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationUser
        fields = '__all__'

class ClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = '__all__'

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email","password"]
    
class FileSystemSerl(serializers.ModelSerializer):
    class Meta:
        model = FileSystem
        fields = "__all__"