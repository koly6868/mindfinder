from django.db import models
from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo
from django.contrib.auth.models import User



#class User(StructuredNode):
#    uid = UniqueIdProperty()
#    name = StringProperty(unique_index=True)
#
#    friends = RelationshipTo('User','FRIEND')



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.CharField('Image path', max_length=255)
    age = models.IntegerField('Age')
    
    friends = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')