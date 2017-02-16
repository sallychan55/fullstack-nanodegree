from handlers.blog_handler import BlogHandler
from modules.comment import Comment

from google.appengine.ext import ndb

class LikePost(BlogHandler):
	#def get(self, post_id):
	#	print "[[GET]] LikePost"

	def post(self, post_id):
		post = ndb.Key('Post', int(post_id)).get()
		self.user.add_like(post)
		print "[[[AFTER add like]]] post.likes: %s" % post.likes
		self.redirect('/blog/%s' % post_id)