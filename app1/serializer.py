from app1.models import PostModel, ChatMessage
from django.contrib.auth.models import User
from .models import UserProfile, UserRating
from rest_framework.serializers import ModelSerializer

class PostModelSerializer(ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'

class ChatMessageSerializer(ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
#filter
#from rest_framework import serializers
# from .models import FilterModel

# class FilterModelSerializer(ModelSerializer):
#     class Meta:
#         model = FilterModel
#         fields = '__all__'

#rating
class UserRatingSerializer(ModelSerializer):
    class Meta:
        model = UserRating
        fields = '__all__'
class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'