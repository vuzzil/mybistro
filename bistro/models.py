from mongoengine import Document, StringField, IntField,DateTimeField
import datetime

class BistroMenu(Document):
    menuid = StringField(max_length=20, unique=True)
    label = StringField(max_length=2)
    title = StringField(max_length=20)
    price = IntField()
    desc = StringField(max_length=200)
    image = StringField(max_length=100)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
    meta = {
        #'db_alias': 'bistrodb',
        'indexes': ['menuid'],
        'ordering': ['-menuid']
    }

    def __str__(self):
        return self.title
