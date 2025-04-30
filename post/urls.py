from django.urls import path
from post.views import PostListAPIView, PostCreateView, PostRetrieveUpdateDestroyView, PostCommentListView, \
    CommentListCreateAPIView

urlpatterns = [
    path('list/', PostListAPIView.as_view()),
    path('create/', PostCreateView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyView.as_view()),
    path('<uuid:pk>/comments/', PostCommentListView.as_view()),
    path('<uuid:pk>/comments/create/', CommentListCreateAPIView.as_view()),
    path('comments/', CommentListCreateAPIView.as_view())
]
