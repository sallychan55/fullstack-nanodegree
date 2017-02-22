from handlers.blog_handler import BlogHandler
from modules.comment import Comment

from google.appengine.ext import ndb

class UnlikePost(BlogHandler):
	#def get(self, post_id):
	#	print "[[GET]] UnlikePost"

	def post(self, post_id):
		post = ndb.Key('Post', int(post_id)).get()
		self.user.remove_like(post)
		print "[[[AFTER REMOVE like]]] post.likes: %s" % post.likes
		self.redirect('/blog/%s' % post_id)