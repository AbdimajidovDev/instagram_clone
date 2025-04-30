from django.core.serializers import serialize
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .models import Post, PostComment, PostLike, CommentLike
from .serializers import PostSerializer, PostLikeSerializer, CommentSerializer, CommentLikeSerializer
from shared.custom_pagination import CustomPagination


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()


class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Post muvoffaqiyatli o'zgartirildi!",
                'data': serializer.data
            }
        )

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(
            {
                'success': True,
                'code': status.HTTP_204_NO_CONTENT,
                'message': "Post muvoffaqiyatli o'chirildi!"
            }
        )


class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post__id=post_id)
        return queryset

class PostCommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = PostComment.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny,]
    queryset = PostComment.objects.all()


class PostLikeListView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [AllowAny, ]
    queryset = PostLike.objects.all()

    def get_object(self):
        post_id = self.kwargs['pk']
        return PostLike.objects.filter(post_id=post_id)


class CommentLikeListView(generics.ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        comment_id = self.kwargs['pk']
        return CommentLike.objects.filter(comment_id=comment_id)


class LikeListView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination
    queryset = PostLike.objects.all()


class PostLikeAPIView(APIView):

    def post(self, reuqest, pk):
        try:
            post_like = PostLike.objects.get(
                author=self.request.user,
                post_id=pk
            )
            post_like.delete()
            data = {
                "success": True,
                'message': "Like qaytarib olindi",
            }
            return Response(data, status=HTTP_204_NO_CONTENT)
        except PostLike.DoesNotExist:
            post_like = PostLike.objects.create(
                author=self.request.user,
                post_id=pk
            )
            serializer = PostLikeSerializer(post_like)
            data = {
                "success": True,
                'message': "Postga like muvoffaqiyatli qo'shildi",
                'data': serializer.data
            }
            return Response(data, status=HTTP_201_CREATED)

    # # # # 2 - usul
    # def post(self, request, pk):
    #     try:
    #         post_like = PostLike.objects.create(
    #             author=self.request.user,
    #             post_id=pk
    #         )
    #         serializer = PostLikeSerializer(post_like)
    #         data = {
    #             'success': True,
    #             'message': "Postga layk muvoffaqiyatli qo'shildi",
    #             'data': serializer.data
    #         }
    #         return Response(data, status=HTTP_201_CREATED)
    #     except Exception as e:
    #         data = {
    #             'success': False,
    #             'message': str(e),
    #             'data': None
    #         }
    #         return Response(data, status=HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk):
    #     try:
    #         post_like = PostLike.objects.get(
    #             author=self.request.user,
    #             post_id=pk
    #         )
    #         post_like.delete()
    #         data = {
    #             'success': True,
    #             'message': "Like muvoffaqiyatli o'chirildi",
    #             'data': None
    #         }
    #         return Response(data, status=HTTP_204_NO_CONTENT)
    #     except Exception as e:
    #         data = {
    #             'success': False,
    #             'message': str(e),
    #             'data': None
    #         }
    #         return Response(data, status=HTTP_400_BAD_REQUEST)




class CommentLikeAPIView(APIView):

    def post(self, request, pk):
        try:
            comment_like = CommentLike.objects.get(
            author=self.request.user,
            comment_id=pk
            )
            comment_like.delete()
            data = {
                'success': True,
                'message': "Izohdan like muvvoffaqiyatli o'chirildi",
                'data': None
            }
            return Response(data, status=HTTP_204_NO_CONTENT)
        except CommentLike.DoesNotExist:
            comment_like = CommentLike.objects.create(
                author=self.request.user,
                comment_id=pk
            )
            serializer = CommentLikeSerializer(comment_like)
            data = {
                        'success': False,
                        'message': "Izohga like muvoffaqiyatli oq'shildi",
                        'data': serializer.data
                    }
            return Response(data, status=HTTP_201_CREATED)



    # # # # keyingi usul
    # def post(self, request, pk):
    #     try:
    #         comment_like = CommentLike.objects.create(
    #             author=self.request.user,
    #             comment_id=pk
    #         )
    #         serializer = CommentLikeSerializer(comment_like)
    #         data = {
    #             'success': True,
    #             'message': "Izohga like muvoffaqiyatli oq'shildi",
    #             'data': serializer.data
    #         }
    #         return Response(data, status=HTTP_201_CREATED)
    #     except Exception as e:
    #         data = {
    #             'success': False,
    #             'message': str(e),
    #             'data': None
    #         }
    #         return Response(data)
    #
    # def delete(self, request, pk):
    #     try:
    #         comment_like = CommentLike.objects.get(
    #             author=self.request.user,
    #             comment_id=pk
    #         )
    #         comment_like.delete()
    #         data = {
    #             'success': True,
    #             'message': "Izohdan like muvvoffaqiyatli o'chirildi",
    #             'data': None
    #         }
    #         return Response(data, status=HTTP_204_NO_CONTENT)
    #     except Exception as e:
    #         data = {
    #             'success': False,
    #             'message': str(e),
    #             'data': None
    #         }
    #         return Response(data, status=HTTP_400_BAD_REQUEST)
