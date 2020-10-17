from rest_framework import serializers
from beakhub.models import BhAccount, BhUser, BhCategory, BhJob, BhAddress


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BhAccount
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BhUser
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BhCategory
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = BhJob
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BhAddress
        fields = '__all__'