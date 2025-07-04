from django.contrib.auth.models import User
from rest_framework import serializers

from communities.models import Profile, Community, Subscriber, Moderator, Topic


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '') # if no email specified the returns ''
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='profile-detail',
        lookup_field='slug'
    )

    class Meta:
        model = Profile
        fields = ['url', 'user', 'display_name', 'image', 'description', 'links']

class CommunitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'

class ModeratorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Moderator
        fields = '__all__'

class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'