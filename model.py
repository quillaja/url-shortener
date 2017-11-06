import datetime as dt
import peewee as pw

_DB = pw.Database('shorturl_test.db')


class Link(pw.Model):
    '''
    Link represents the association between a full url and a unique key
    which is used to access the url.
    '''
    created = pw.DateTimeField(default=dt.datetime.now)
    modified = pw.DateTimeField()
    key = pw.CharField()
    url = pw.CharField()
    clicked = pw.IntegerField(default=0)

    def save(self):
        self.modified = dt.datetime.now()
        super().save()


def create_database():
    _DB.connect()
    _DB.create_tables([Link], safe=True)
    _DB.close()
