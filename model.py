import datetime as dt
import peewee as pw
import random

_DB = pw.SqliteDatabase('shorturl_test.db')


def create_key(length: int=8) -> str:
    b64_alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$+"
    key = random.choices(b64_alphabet, k=length)
    return ''.join(key)


class Link(pw.Model):
    '''
    Link represents the association between a full url and a unique key
    which is used to access the url.
    '''
    created = pw.DateTimeField(default=dt.datetime.now)
    modified = pw.DateTimeField()
    key = pw.CharField(unique=True, default=create_key)
    url = pw.CharField(unique=True)
    clicked = pw.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.modified = dt.datetime.now()
        super().save(*args, **kwargs)

    class Meta(object):
        database = _DB


def create_database():
    _DB.connect()
    _DB.create_tables([Link], safe=True)
    _DB.close()
