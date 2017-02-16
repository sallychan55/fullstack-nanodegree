import random
from string import letters
import hashlib

from google.appengine.ext import ndb

from comment import Comment

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return ndb.Key('users', group)

class User(ndb.Model):
    name = ndb.StringProperty(required = True)
    pw_hash = ndb.StringProperty(required = True)
    email = ndb.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.query(User.name == name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

    def add_comment(self, comment, post):
        return Comment.create(comment, self, post) 

    def is_editable(self, obj):
        return self.key == obj.author;

    def get_displayname(self):
        return self.name

    def add_like(self, post):
        if self.can_like_post(post):
            return post.add_like(self)

    def remove_like(self, post):
        if self.can_unlike_post(post):
            return post.remove_like(self)        

    def liked_post(self, post):
        return self.key in post.likes    

    def can_like_post(self, post):
        return self.key != post.author and not self.liked_post(post) 

    def can_unlike_post(self, post):
        return self.key != post.author and self.liked_post(post)                