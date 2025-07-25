from django.contrib.auth.models import User
from rest_framework import serializers

from communities.models import Profile, Community, Subscriber, Moderator, Topic, Comment, TopicVote, Notification, Ban


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
        read_only=True
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='profile-detail',
        lookup_field='slug'
    )

    class Meta:
        model = Profile
        fields = ['url', 'user', 'display_name', 'image', 'description', 'links', 'karma']

class CommunitySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='community-detail',
        lookup_field='slug'
    )

    class Meta:
        model = Community
        fields = ['url', 'name', 'image', 'description', 'slug', 'subscriber_count', 'total_view_count']

class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'

class ModeratorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Moderator
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='comment-detail'
    )
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    topic = serializers.HyperlinkedRelatedField(
        queryset=Topic.objects.all(),
        view_name='topic-detail',
        lookup_field='slug',
    )
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['url', 'id', 'topic', 'text', 'created_date', 'user', 'vote_count', 'upper_comment', 'replies']

    def get_replies(self, obj):
        serializer = CommentSerializer(obj.replies.all(), many=True, context=self.context)
        return serializer.data

class TopicSerializer(serializers.HyperlinkedModelSerializer):
    community = serializers.HyperlinkedRelatedField(
        queryset=Community.objects.all(),
        view_name='community-detail',
        lookup_field='slug'
    )
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='topic-detail',
        lookup_field='slug'
    )
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['url', 'community', 'title', 'text', 'image', 'created_date', 'user',
                  'vote_count', 'view_count', 'comments', 'slug']

    def get_comments(self, obj):
        top_comments = obj.comments.filter(upper_comment__isnull=True).order_by('created_date')
        return CommentSerializer(top_comments, many=True, read_only=True, context=self.context).data


class BanSerializer(serializers.HyperlinkedModelSerializer):
    community = serializers.HyperlinkedRelatedField(
        queryset=Community.objects.all(),
        view_name='community-detail',
        lookup_field='slug'
    )
    user = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name='user-detail',
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='ban-detail',
    )

    class Meta:
        model = Ban
        fields = ['url', 'user', 'community', 'created_at', 'expires_at', 'is_active']