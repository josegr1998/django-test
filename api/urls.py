from django.urls import path
from . import views

urlpatterns = [
    path('blogposts/',views.BlogPostListCreate.as_view(),name='blogpost-view-create'),
    path('blogposts/<int:pk>/',views.BlogPostRetrieveUpdateDestroy.as_view(),name='blogpost-retrieve-update-destroy'),
    path('users/',views.UserListCreate.as_view(),name='user-list-create'),
    path('users/<int:pk>/',views.UserRetrieveUpdateDestroy.as_view(),name='user-retrieve-update-destroy'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
]