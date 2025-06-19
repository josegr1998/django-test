import django_filters
from .models import BlogPost
from rest_framework.exceptions import ValidationError

class BlogPostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(method='filter_title')
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains')
    published_date = django_filters.DateFilter(field_name='published_at', lookup_expr='gte')
    
    def filter_title(self, queryset, name, value):
        # Extra validation (e.g., must be in the past)
        if len(value) < 3:
            raise ValidationError({"message": "Title must be at least 3 characters long."})
        return queryset.filter(**{name + '__icontains': value})

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'published_date']