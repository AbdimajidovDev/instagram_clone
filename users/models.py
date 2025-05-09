import random
import uuid
from datetime import datetime, timedelta
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

from shared.models import BaseModel


ORDINARY_USER, MANAGER,ADMIN = ("ordinary_user", 'manager', 'admin')
VIA_EMAIL, VIA_PHONE = ('email', 'phone')
NEW, CODE_VERIFIED, DONE, PHOTO_DONE = ('new', 'code_verified', 'done', 'photo_done')

class User(AbstractUser, BaseModel):
    USER_ROLES = (
        (ORDINARY_USER, ORDINARY_USER),
        (MANAGER, MANAGER),
        (ADMIN, ADMIN),
    )

    AUTH_TYPE_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )

    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE)
    )

    user_role = models.CharField(max_length=33, choices=USER_ROLES, default=ORDINARY_USER)
    auth_type = models.CharField(max_length=33, choices=AUTH_TYPE_CHOICES)
    auth_status = models.CharField(max_length=33, choices=AUTH_STATUS, default=NEW)

    email = models.EmailField(null=True, unique=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'heif'])])

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def create_verify_code(self, verify_type):
        code = "".join([str(random.randint(0, 100) % 10) for i in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id,
            verify_type=verify_type,
            code=code
        )
        return code

    # vaqtincha username yaratish - username ustuni bo'sh bo'lmasligi shart. user birinchi email yoki phone orqali
    # ro'yxatdan o'tganda uning usernamesi bo'lmaydi bu funksiya shuning uchun
    def check_username(self):

        if not self.username:
            # uuid.uuid4.__str__() -> c303282d-f2e6-46ca-a04a-35d3d873712d (takrorlanmas kod yasab beradi)
            temp_username = f"instagram-{uuid.uuid4().__str__().split('-')[-1]}"  # instagram-35d3d873712d
            while User.objects.filter(username=temp_username):  # moboda takrorlanib qolsa
                temp_username = f"{temp_username}{random.randint(0, 9)}"  # ohiridan raqam qo'shib boriladi
            self.username = temp_username

    def check_email(self):

        if self.email:
            normalize_email = self.email.lower() # AliVali@gmail.com ->  alivali@gmail.com
            self.email = normalize_email

    def check_pass(self): # vaqtincha pass yaratish: password ham majburiy field bolgani uchun
        if not self.password:  # agar passwor bo'lmasa
            temp_password = f"password-{uuid.uuid4().__str__().split('-')[-1]}"  # password yaratadi
            self.password = temp_password # yaratildi (password takrorlanmas bo'lishi shart emas)

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'): # pbkdf2_sha256 -> djangoning default heshlashi
            self.set_password(self.password)  # parolni heshlash

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

    def clean(self):
        self.check_email()
        self.check_username()
        self.check_pass()
        self.hashing_password()

    def save(self, *args, **kwargs):
        # if not self.pk:
        self.clean()
        super(User, self).save(*args, **kwargs)



PHONE_EXPIRE = 2
EMAIL_EXPIRE = 5

class UserConfirmation(BaseModel):
    TYPE_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )
    code = models.CharField(max_length=4)
    verify_type = models.CharField(max_length=33, choices=TYPE_CHOICES)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs):

        if self.verify_type == VIA_EMAIL:
            self.expiration_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRE)
        else:
            self.expiration_time = datetime.now() + timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)


