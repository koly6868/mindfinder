from django.urls import path

from . import views

app_name='user_service'

urlpatterns = [
    path('profile/', views.UserProfile.as_view(), name='profile'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signin/', views.SignIn.as_view(), name='signin'),
]