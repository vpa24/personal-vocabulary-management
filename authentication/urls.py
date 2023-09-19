from .views import RegistrationView, UsernameValidationView, EmailValidationView, LogoutView, VerificationView, LoginView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as autth_views

urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()),
         name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()),
         name='validate_email'),
    path('activate/<uidb64>/<token>',
         VerificationView.as_view(), name='activate'),
    path('reset-password', autth_views.PasswordResetView.as_view(template_name="authentication/password_reset.html"),
         name="reset_password"),
    path('reset-password-send', autth_views.PasswordResetDoneView.as_view(template_name="authentication/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>', autth_views.PasswordResetConfirmView.as_view(template_name="authentication/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset-password-complete', autth_views.PasswordResetCompleteView.as_view(template_name="authentication/password_reset_done.html"),
         name="password_reset_complete")

]
