from handlers.blog_handler import BlogHandler
from modules.comment import Comment
from modules.validation import user_owns_comment

from google.appengine.ext import ndb

class DeleteComment(BlogHandler):
    @user_owns_comment
    def get(self, comment):
		self.render("deletecomment.html", comment=comment)

    @user_owns_comment
    def post(self, comment):
		comment.delete()
		self.render("deletecomment.html", comment=comment, deleted=True)