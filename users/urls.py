from django.urls import path
from .views import (CreateUserView, VerifyAPIView,
                    GetNewVerification, ChangeUserInformationView,
                    ChangeUserPhotoView, LoginView,
                    LoginRefreshView, LogOutView, ForgetPasswordView, )

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('login/refresh/', LoginRefreshView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
    path('new-verify/', GetNewVerification.as_view()),
    path('change-user/', ChangeUserInformationView.as_view()),
    path('change-user-photo/', ChangeUserPhotoView.as_view()),
    path('forgot-password/', ForgetPasswordView.as_view()),
]
