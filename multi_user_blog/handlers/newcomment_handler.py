from handlers.blog_handler import BlogHandler
from modules.user import User
from modules.comment import Comment
from modules.validation import user_owns_post

from google.appengine.ext import ndb

class NewComment(BlogHandler):
    @user_owns_post
    def get(self, post):
        self.render("newcomment.html", post_id=post.key.id())

    @user_owns_post
    def post(self, post):
		comment = self.request.get("comment")
	
		if comment:
			self.user.add_comment(comment, post)
            self.redirect('/blog/%s' % post.key.id())
        else:
			error = "Please add content!"
            self.render("newcomment.html", comment=comment, post_id=post.key.id(), error=error)
