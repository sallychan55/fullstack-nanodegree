from handlers.blog_handler import BlogHandler
from modules.comment import Comment

from google.appengine.ext import ndb

class EditComment(BlogHandler):
	def get(self, comment_key):
        if not self.user:
            self.redirect("/login")

		comment = ndb.Key(urlsafe=comment_key).get()	
		self.render("editcomment.html", comment=comment)

	def post(self, comment_key):
		# TODO: is there any better way to get comment by id?
        # comment = Comment.get_by_id(comment_key, parent=p_key)

        if not self.user:
            self.redirect("/login")

		new_comment = self.request.get("new_comment")
		comment = ndb.Key(urlsafe=comment_key).get()	

		if new_comment and comment:
			comment.comment = new_comment
			comment.put()
			#comment.update(new_comment) <-- somehow it doesn't work to update data
			self.render("editcomment.html", comment=comment, updated=True)	
		else:
			error = "Please add comment!"
			self.render("editcomment.html", comment=comment, error=error)