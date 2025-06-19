from rest_framework import serializers
from .models import BlogPost

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
        fields = ['id', 'title', 'content', 'published_date']