from handlers.blog_handler import BlogHandler
from modules.comment import Comment
from modules.validation import user_owns_comment

from google.appengine.ext import ndb

class EditComment(BlogHandler):
    @user_owns_comment
    def get(self, comment):
		self.render("editcomment.html", comment=comment)

    @user_owns_comment
    def post(self, comment):
		new_comment = self.request.get("new_comment")

    if new_comment:
			comment.comment = new_comment
			comment.put()
			#comment.update(new_comment) <-- somehow it doesn't work to update data
			self.render("editcomment.html", comment=comment, updated=True)	
		else:
			error = "Please add comment!"
			self.render("editcomment.html", comment=comment, error=error)