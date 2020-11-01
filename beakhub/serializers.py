from rest_framework import serializers
from beakhub.models import BhAccount, BhUser, BhCategory, BhJob, BhAddress


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BhAccount
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BhUser
        fields = ['account', 'first_name', 'last_name', 'email', 'whatsapp_phone', 'phone_number',
                  'profile_picture','created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BhCategory
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    class Meta:
        model = BhJob
        fields = ['id', 'title', 'description', 'is_active', 'created_at', 'updated_at', 'user', 'user_id', 'category', 'category_id']
    def create(self, validated_data):
        validated_data['category'] = BhCategory.objects.get(id=self.context['request'].data['category_id'])
        validated_data['user'] = BhUser.objects.get(account_id=self.context['request'].data['user_id'])
        return super(JobSerializer, self).create(validated_data)

class AddressSerializer(serializers.ModelSerializer):
    job = serializers.StringRelatedField()
    class Meta:
        model = BhAddress
        fields = ['id', 'title', 'country', 'town', 'street', 'website', 'phone_number_1',
                  'phone_number_2', 'job', 'job_id']
    def create(self, validated_data):
        validated_data['job'] = BhJob.objects.get(id=self.context['request'].data['job_id'])
        return super(AddressSerializer, self).create(validated_data)