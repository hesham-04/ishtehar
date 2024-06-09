from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('setup/', views.SetupView.as_view(), name='setup'),
]