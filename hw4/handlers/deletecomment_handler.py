from handlers.blog_handler import BlogHandler
from modules.comment import Comment

from google.appengine.ext import ndb

class DeleteComment(BlogHandler):
	def get(self, comment_key):
        if not self.user:
            self.redirect("/login")

		comment = ndb.Key(urlsafe=comment_key).get()
		self.render("deletecomment.html", comment=comment)

	def post(self, comment_key):
        if not self.user:
            self.redirect("/login")

		comment = ndb.Key(urlsafe=comment_key).get()	
		comment.delete()
		self.render("deletecomment.html", comment=comment, deleted=True)