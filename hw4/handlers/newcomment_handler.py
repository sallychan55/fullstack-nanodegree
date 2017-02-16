from handlers.blog_handler import BlogHandler
from modules.user import User
from modules.comment import Comment

from google.appengine.ext import ndb

class NewComment(BlogHandler):
	def get(self, post_id):
		self.render("newcomment.html", post_id=post_id)

	def post(self, post_id):
		comment = self.request.get("comment")
	
		if comment:
			post = ndb.Key('Post', int(post_id)).get()
			self.user.add_comment(comment, post)
			self.redirect('/blog/%s' % post_id)	
		else:
			error = "Please add content!"
			self.render("newcomment.html", comment=comment, post_id=post_id, error=error)	