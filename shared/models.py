from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True) # UUIDField id field un,default=uuid.uuid4 -> id yaratib beradi, takrorlanmas id yaratish uchun, editable=False -> o'zgartirib bo'lmasligi uchun
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
