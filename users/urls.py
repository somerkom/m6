from django.urls import path
from .views import AuthorizationAPIView, RegistrationAPIView, ConfirmUserAPIView

urlpatterns = [
    path('auth/', AuthorizationAPIView.as_view(), name='auth'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('confirm/', ConfirmUserAPIView.as_view(), name='confirm'),
]