from django.urls import path
from .views import AccountRegisterAPIView, LoginAPIView, ResetPasswordAPIView, SetPasswordConfirmAPIView, \
    SetNewPasswordCompletedAPIView, MyAccountAPIView, EmailVerificationAPIView

urlpatterns = [
    path('register/', AccountRegisterAPIView.as_view()),

    path('verify-email/', EmailVerificationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('reset-password/', ResetPasswordAPIView.as_view()),
    path('set-password-confirm/<str:uidb64>/<str:token>/', SetPasswordConfirmAPIView.as_view()),
    path('set-password-completed/', SetNewPasswordCompletedAPIView.as_view()),
    path('profile/<str:username>/', MyAccountAPIView.as_view()),
]
