from rest_framework import serializers
from MoviesAndMe.models import movie_detail, tv_detail
from django.contrib.auth.models import User


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
