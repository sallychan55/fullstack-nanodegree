from handlers.blog_handler import BlogHandler
from modules.validation import user_owns_post

from google.appengine.ext import ndb

class DeletePost(BlogHandler):
    @user_owns_post
    def get(self, post):
        self.render("deletepost.html", p=post)

    @user_owns_post
    def post(self, post):
        post.delete()
        self.render("deletepost.html", p=post, deleted=True) 