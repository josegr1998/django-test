from rest_framework import serializers
from .models import BlogPost, CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

class BlogPostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=True)


    def validate(self, data):
        if self.instance:  # Means it's an update, not a create
            required_fields = ['title', 'content']
            for field in required_fields:
                if field not in data or not data.get(field):
                    raise serializers.ValidationError({field: f"{field} is required for updates."})
        return data

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'published_date', 'author']





class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'posts']

    def get_posts(self, obj):
        expand = self.context.get('expand_posts', False)
        print("🔍 Expand parameter:", expand)  # ✅ This will now log
        if expand:
            return BlogPostSerializer(obj.posts.all(), many=True, context=self.context).data
        return [post.id for post in obj.posts.all()]
    

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'bio']  # customize this

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user