from google.appengine.ext import ndb


class Devices(ndb.Model):
    deviceId = ndb.StringProperty()
    pushKey = ndb.StringProperty()