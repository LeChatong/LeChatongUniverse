from rest_framework import serializers
from django.contrib.auth.models import User
from lcu.models import member, movie_detail, tv_detail


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = movie_detail
        fields = '__all__'

class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = tv_detail
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MembeSerializer(serializers.ModelSerializer):
    class Meta:
        model = member
        fields = '__all__'