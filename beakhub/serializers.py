from django.utils.timezone import utc
from rest_framework import serializers
from beakhub.models import BhAccount, BhUser, BhCategory, BhJob, BhAddress, BhComment, BhUserLikeJob, BhEvent
from django.conf import settings
from datetime import datetime


class AccountSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S', default=datetime.now())
    updated_at = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S', default=datetime.now())
    last_login = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S', default=datetime.now())
    class Meta:
        model = BhAccount
        fields = ['id', 'username', 'password', 'last_login', 'is_active', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    url_picture = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S', default=datetime.now())
    updated_at = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S', default=datetime.now())

    def get_url_picture(self, instance):
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
    number_comment = serializers.SerializerMethodField()
    number_like = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S', default=datetime.now())
    updated_at = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S', default=datetime.now())

    class Meta:
        model = BhJob
        fields = ['id', 'title', 'description', 'is_active', 'created_at', 'updated_at',
                  'user', 'user_id', 'category', 'category_id', 'number_comment', 'number_like']

    def create(self, validated_data):
        validated_data['category'] = BhCategory.objects.get(id=self.context['request'].data['category_id'])
        validated_data['user'] = BhUser.objects.get(account_id=self.context['request'].data['user_id'])
        return super(JobSerializer, self).create(validated_data)

    def get_number_comment(self, instance):
        comments = BhComment.objects.filter(job_id=instance.id)
        return len(comments)

    def get_number_like(self, instance):
        likes_job = BhUserLikeJob.objects.filter(job_id=instance.id, is_like=True)
        return len(likes_job)

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
    created_at = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S',default=datetime.now())
    updated_at = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S',default=datetime.now())

    class Meta:
        model = BhComment
        fields = ['id', 'commentary', 'user', 'user_id', 'job', 'job_id', 'is_active', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['job'] = BhJob.objects.get(id=self.context['request'].data['job_id'])
        validated_data['user'] = BhUser.objects.get(account_id=self.context['request'].data['user_id'])
        return super(CommentSerializer, self).create(validated_data)

class BhUserLikeJobSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    job = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S', default=datetime.now())
    updated_at = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S', default=datetime.now())

    class Meta:
        model = BhUserLikeJob
        fields = ['id', 'is_like', 'user', 'user_id', 'job', 'job_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['job'] = BhJob.objects.get(id=self.context['request'].data['job_id'])
        validated_data['user'] = BhUser.objects.get(account_id=self.context['request'].data['user_id'])
        return super(BhUserLikeJobSerializer, self).create(validated_data)

class BhEventSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d %b %Y %H:%M:%S', default=datetime.now())
    #updated_at = serializers.DateTimeField(format='%a, %d %b %Y %H:%M:%S', default=datetime.now())
    job_title = serializers.SerializerMethodField()
    name_sender = serializers.SerializerMethodField()
    url_picture_sender = serializers.SerializerMethodField()
    how_hours = serializers.SerializerMethodField()
    class Meta:
        model = BhEvent
        fields = ['id', 'reciever_id', 'sender_id', 'action', 'is_view', 'job_id', 'created_at', 'updated_at',
                  'job_title', 'name_sender', 'url_picture_sender', 'how_hours']
    def get_job_title(self, instance):
        job = BhJob.objects.get(id=instance.job_id)
        return job.title
    def get_name_sender(self, instance):
        sender = BhUser.objects.get(account_id=instance.sender_id)
        return sender.first_name + ' ' + sender.last_name
    def get_url_picture_sender(self, instance):
        sender = BhUser.objects.get(account_id=instance.sender_id)
        return settings.SITE_URL+sender.profile_picture.url if sender.profile_picture else ''
    def get_how_hours(self, instance):
        FMT= "%H"
        diff_date = datetime.now(utc) - instance.updated_at
        return diff_date.days * 24 + diff_date.seconds // 3600

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
