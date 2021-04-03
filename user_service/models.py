from django.db import models
from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo
from django.contrib.auth.models import User

MESSAGE_MAX_LEN = 8192


#class User(StructuredNode):
#    uid = UniqueIdProperty()
#    name = StringProperty(unique_index=True)
#
#    friends = RelationshipTo('User','FRIEND')



class UserProfile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)

    avatar = models.CharField('Image path', max_length=255)
    age = models.IntegerField('Age')
    
    friends = models.ForeignKey(User)

    

class Message(models.Model):
    datetime = models.DateTimeField('Message sent datetime', auto_now=True)
    message = models.CharField('Message', max_length=MESSAGE_MAX_LEN, blank=False)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)



class Chat(models.Model):
    start_date = models.DateTimeField('Chat start datetime', auto_now=True)
    messages = models.ForeignKey(Message, on_delete=models.CASCADE)
    participants = models.ForeignKey(User)