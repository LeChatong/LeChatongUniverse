from rest_framework import serializers
from .models import movie_detail, tv_detail


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = movie_detail
        fields = '__all__'

class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = tv_detail
        fields = '__all__'
