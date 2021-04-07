from django.urls import path

from . import views

app_name='chat_service'

urlpatterns = [
    path('chats/', views.ChatListView.as_view(), name='chats'),
    path('chats/<int:chat_id>', views.ChatView.as_view(), name='chat'),
    path('chats/new', views.CreateChatView.as_view(), name='new'),
]