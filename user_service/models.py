from django.db import models
from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo

# Create your models here.

class User(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)

    friends = RelationshipTo('Person','FRIEND')