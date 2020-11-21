from rest_framework import serializers
from beakhub.models import BhAccount, BhUser, BhCategory, BhJob, BhAddress, BhComment
from django.conf import settings


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BhAccount
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    url_picture = serializers.SerializerMethodField()
    def get_url_picture(self, instance):
        # returning image url if there is an image else blank string
        return settings.SITE_URL+instance.profile_picture.url if instance.profile_picture else ''
    class Meta:
        model = BhUser
        fields = ['account_id', 'first_name', 'last_name', 'email', 'whatsapp_phone', 'phone_number',
                  'url_picture', 'account','created_at', 'updated_at']

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
                  'phone_number_2', 'job', 'job_id', 'is_active', 'created_at', 'updated_at']
    def create(self, validated_data):
        validated_data['job'] = BhJob.objects.get(id=self.context['request'].data['job_id'])
        return super(AddressSerializer, self).create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    job = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S')
    class Meta:
        model = BhComment
        fields = ['id', 'commentary', 'user', 'user_id', 'job', 'job_id', 'is_active', 'created_at', 'updated_at']
    def create(self, validated_data):
        validated_data['job'] = BhJob.objects.get(id=self.context['request'].data['job_id'])
        validated_data['user'] = BhUser.objects.get(account_id=self.context['request'].data['user_id'])
        return super(CommentSerializer, self).create(validated_data)


class APIResponse:
    def __init__(self, MESSAGE, DATA, CODE, ERRORS):
        self.MESSAGE = MESSAGE
        self.DATA = DATA
        self.CODE = CODE
        self.ERRORS = ERRORS

class APIResponseSerialiser(serializers.Serializer):
    MESSAGE = serializers.CharField()
    DATA    = serializers.JSONField()
    CODE    = serializers.IntegerField()
