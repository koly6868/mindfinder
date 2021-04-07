from django.urls import path

from . import views

app_name='user_service'

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]