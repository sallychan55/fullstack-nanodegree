import os
import re
import random
import hashlib
import hmac
from string import letters

import webapp2

from handlers.blog_handler import BlogHandler
from handlers.editpost_handler import EditPost
from handlers.deletepost_handler import DeletePost
from handlers.newcomment_handler import NewComment
from handlers.editcomment_handler import EditComment
from handlers.deletecomment_handler import DeleteComment
from handlers.likepost_handler import LikePost
from handlers.unlikepost_handler import UnlikePost

from modules.post import Post
from modules.user import User
from modules.comment import Comment

from google.appengine.ext import ndb

class MainPage(BlogHandler):
  def get(self):
      self.write('Hello, Udacity!')

class BlogFront(BlogHandler):
    def get(self):
        posts = Post.query().order(-Post.created).fetch()
        if self.user:
            self.render('front.html', posts=posts, user=self.user)
        elif not self.user:
            self.render('front.html', posts=posts)
   
class PostPage(BlogHandler):
    def get(self, post_id):
        post = ndb.Key('Post', int(post_id)).get()
        
        if not post:
            self.error(404)
            return self.render("not_found.html")

        self.render("permalink.html", post = post, user = self.user)

class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        elif not self.user:
            self.redirect("/login") 

    def post(self):
        if not self.user:
            self.redirect('/login')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post_key = Post.create(subject = subject, content = content, author = self.user)
            self.redirect('/blog/%s' % str(post_key.id()))
        else:
            error = "Please add subject and content!"
            self.render("newpost.html", subject=subject, content=content, error=error)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(BlogHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

class Register(Signup):
    def done(self):
        # make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/')

class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password) # Check username/password
        if u:
            self.login(u) # Set-Cookie
            self.redirect('/')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/')

class Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.redirect('/blog')
        else:
            self.redirect('/signup')


app = webapp2.WSGIApplication([('/', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/edit/post_id:([0-9]+)', EditPost),
                               ('/delete/post_id:([0-9]+)', DeletePost),
                               ('/newcomment/post_id:([0-9]+)', NewComment),
                               webapp2.Route('/editcomment/<comment_key:[a-zA-Z0-9_-]+>',
                                             handler=EditComment,
                                             name='editcomment'),
                               webapp2.Route('/deletecomment/<comment_key:[a-zA-Z0-9_-]+>',
                                             handler=DeleteComment,
                                             name='deletecomment'),
                               webapp2.Route('/likepost/<post_id:[0-9]+>',
                                             handler=LikePost,
                                             name='likepost'),
                               webapp2.Route('/unlikepost/<post_id:[0-9]+>',
                                             handler=UnlikePost,
                                             name='unlikepost')
                               ],
                              debug=True)