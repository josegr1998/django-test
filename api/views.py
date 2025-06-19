from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer
from .filters import BlogPostFilter
import logging

logger = logging.getLogger(__name__)


class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BlogPostFilter

    print("🔥 Class loaded")  # Will print when Django loads the class

    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())


        if not queryset.exists():
            return Response(
                {"message": "No blog posts found matching the filters."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset, many=True)

        
        print("🔍 Overridden get() called")
        print("Serialized blog post omgs:", serializer.data)
        return Response(serializer.data)


class BlogPostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'pk'