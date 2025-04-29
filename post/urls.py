from django.urls import path
from post.views import PostListAPIView, PostCreateView, PostRetrieveUpdateDestroyView

urlpatterns = [
    path('posts/', PostListAPIView.as_view()),
    path('posts/create/', PostCreateView.as_view()),
    path('posts/<uuid:pk>/', PostRetrieveUpdateDestroyView.as_view()),
]
