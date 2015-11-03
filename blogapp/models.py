from mongoengine import *
from simpleblog.settings import DBNAME
from mongoengine.django.storage import GridFSStorage
import datetime

connect(DBNAME)


class Img(Document):
    img_src = FileField()
    img_width = IntField(min_value = 1)
    img_height = IntField(min_value = 1)
	
class User(Document):
	username = StringField(max_length=30, required=True)
	password = StringField(max_length=30, required=True)
	security_level = IntField(default=1, required=True)
	is_verify = BooleanField(default=False, required=True)
	

#Post contains title, content, and date_added
class Post(Document):
    title = StringField(max_length=100, required=True)
    content = StringField(max_length=1000, required=True)
    date_added = DateTimeField(default=datetime.datetime.now, required=True)
    image_id = ReferenceField(Img)
    author = ReferenceField(User)
    VIEWABLE = (('P', 'public'), ('N', 'network'))
    viewable = StringField(max_length=1, min_length=1, choices=VIEWABLE, required=True)

