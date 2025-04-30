from django.urls import path
from post.views import (PostListAPIView,
                        PostCreateView,
                        PostRetrieveUpdateDestroyView,
                        PostCommentListView,
                        CommentListCreateAPIView,
                        PostLikeListView,
                        CommentRetrieveAPIView,
                        CommentLikeListView,
                        LikeListView, PostLikeAPIView, CommentLikeAPIView, )

urlpatterns = [
    path('list/', PostListAPIView.as_view()),
    path('create/', PostCreateView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyView.as_view()),

    path('likes/', LikeListView.as_view()),
    path('<uuid:pk>/likes/', PostLikeListView.as_view()),
    path('comments/<uuid:pk>/likes/', CommentLikeListView.as_view()),

    path('<uuid:pk>/comments/', PostCommentListView.as_view()),
    path('<uuid:pk>/comments/create/', CommentListCreateAPIView.as_view()),

    path('comments/', CommentListCreateAPIView.as_view()),
    path('comments/<uuid:pk>/', CommentRetrieveAPIView.as_view()),
    path('<uuid:pk>/create-delete-like/', PostLikeAPIView.as_view()),
    path('comments/<uuid:pk>/create-delete-like/', CommentLikeAPIView.as_view()),
]
