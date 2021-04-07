from django.db import models
from neomodel import StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo
from django.contrib.auth.models import User
from mindfinder.settings import MEDIA_ROOT
from django.core.files.storage import FileSystemStorage


DEFAULT_AVATAR_IMAGE = 'avatars/no_photo_icon.png'


# class User(StructuredNode):
#    uid = UniqueIdProperty()
#    name = StringProperty(unique_index=True)
#
#    friends = RelationshipTo('User','FRIEND')


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE)

    avatar = models.ImageField(
        storage=FileSystemStorage(location=MEDIA_ROOT),
        upload_to='avatars',
        default=DEFAULT_AVATAR_IMAGE)
    name = models.CharField(
        'Name',
        max_length=255,
        default='')
    age = models.IntegerField(
        'Age',
        null=True)

    friends = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+',
        null=True)
