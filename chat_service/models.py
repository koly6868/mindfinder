from django.db import models
from django.contrib.auth.models import User


MESSAGE_MAX_LEN = 8192



class Chat(models.Model):
    participants = models.ManyToManyField(User)
    start_date = models.DateTimeField('Chat start datetime', auto_now=True)



class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.CharField('Message', max_length=MESSAGE_MAX_LEN, blank=False)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField('Message sent datetime', auto_now=True)


