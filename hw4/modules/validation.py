from functools import wraps

from google.appengine.ext import ndb


def post_exists(f):
    @wraps(f)
    def wrapper(self, post_id, *a, **kw):
        post = ndb.Key('Post', int(post_id)).get()
        if post:
            return f(self, post, *a, **kw)
        else:
            self.render("not_found.html")

    return wrapper


def user_logged_in(f):
    @wraps(f)
    def wrapper(self, *a, **kw):
        if self.user:
            return f(self, *a, **kw)
        else:
            return self.redirect("/login")

    return wrapper


def user_owns_post(f):
    @wraps(f)
    @post_exists
    @user_logged_in
    def wrapper(self, post, *a, **kw):
        if self.user.key == post.author:
            return f(self, post, *a, **kw)
        else:
            return self.render("not_found.html")

    return wrapper


def comment_exists(f):
    @wraps(f)
    def wrapper(self, comment_key, *a, **kw):
        comment = ndb.Key(urlsafe=comment_key).get()
        if comment:
            return f(self, comment, *a, **kw)
        else:
            self.render("not_found.html")

    return wrapper


def user_owns_comment(f):
    @wraps(f)
    @comment_exists
    @user_logged_in
    def wrapper(self, comment, *a, **kw):
        if self.user.key == comment.author:
            return f(self, comment, *a, **kw)
        else:
            return self.render("not_found.html")

    return wrapper
