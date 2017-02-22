from handlers.blog_handler import BlogHandler
from modules.validation import user_owns_post

from google.appengine.ext import ndb

class EditPost(BlogHandler):
    @user_owns_post
    def get(self, post):
        self.render("editpost.html", p=post)

    @user_owns_post
    def post(self, post):
        subject = self.request.get('subject')
        content = self.request.get('content')
        key_id = self.request.get('key_id')
       
        if subject and content:
            post.update(subject, content)
            self.render("editpost.html", p=post, updated=True)
        elif not subject:
            error = "Please add subject!"
            self.render("editpost.html", p=post, subject=subject, content=content, error=error, errors=True)
        else:
            error = "Please add comment!"
            self.render("editpost.html", p=post, subject=subject, content=content, error=error, errors=True)
