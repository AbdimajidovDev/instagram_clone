from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db import models
from django.db.models import UniqueConstraint

from shared.models import BaseModel


User = get_user_model()


class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts_images',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    caption = models.TextField(validators=[MaxLengthValidator(2000)])

    class Meta:
        db_table = "posts"
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return f"{self.author} post about {self.caption}"


class PostComment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child', null=True, blank=True)

    class Meta:
        db_table = "post_comments"
        verbose_name = "post comment"
        verbose_name_plural = "post comments"

    def __str__(self):
        return f"{self.author}: {self.comment[:30]}"


class PostLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        db_table = "post_likes"
        verbose_name = "post like"
        verbose_name_plural = "post likes"
        constraints = [
            UniqueConstraint(
                fields=['author', 'post'],
                name='PostLikeUnique')
        ]


class CommentLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        db_table = "comment_likes"
        verbose_name = "comment like"
        verbose_name_plural = "comment likes"
        constraints = [
            UniqueConstraint(
                fields=['author', 'comment'],
                name='CommentLikeUnique')
        ]
