from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register_user_view, name='register_user'),
    path("verify-email/",views.verify_email_view, name="verify_email")
]