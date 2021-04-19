from django.db import models
from user_service.models import UserProfile


MESSAGE_MAX_LEN = 8192
CHAT_MAX_LEN = 255


class Chat(models.Model):
    name = models.CharField('Chat name', max_length=CHAT_MAX_LEN)
    participants = models.ManyToManyField(UserProfile)
    start_date = models.DateTimeField('Chat start datetime', auto_now=True)



class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.CharField('Message', max_length=MESSAGE_MAX_LEN, blank=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    datetime = models.DateTimeField('Message sent datetime', auto_now=True)


