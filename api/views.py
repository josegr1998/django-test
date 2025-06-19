from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response
from .models import BlogPost, CustomUser
from .serializers import BlogPostSerializer, UserSerializer, RegisterSerializer
from .filters import BlogPostFilter
import logging
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)

User = get_user_model()


class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BlogPostFilter
    authentication_classes = [JWTAuthentication]  # <- Add this
    permission_classes = [IsAuthenticated]    

    print("🔥 Class loaded")  # Will print when Django loads the class

    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())


        if not queryset.exists():
            return Response(
                {"message": "No blog posts found"},
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


class UserListCreate(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        expand_param = self.request.query_params.get('expand_posts', 'false').lower()
        context['expand_posts'] = expand_param in ['1', 'true', 'yes']
        return context

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if not queryset.exists():
            return Response(
                {"message": "No users found"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(serializer.data)

class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # ✅ Allow access without authentication

    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "token": str(token.access_token)
        }, status=status.HTTP_201_CREATED)


from rest_framework.views import APIView

class LoginView(APIView):
    permission_classes = [AllowAny]  # ✅ Allow access without authentication

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "token": str(token.access_token)
        })