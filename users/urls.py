from django.urls import path
from .views import CreateUserView, VerifyAPIView, GetNewVerification, ChangeUserInformationView, ChangeUserPhotoView

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
    path('new-verify/', GetNewVerification.as_view()),
    path('change-user/', ChangeUserInformationView.as_view()),
    path('change-user-photo/', ChangeUserPhotoView.as_view()),
]
