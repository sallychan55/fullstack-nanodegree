from google.appengine.ext import ndb

class Comment(ndb.Model):
	comment = ndb.TextProperty(required=True)
	author = ndb.KeyProperty("User", required=True) 
	created = ndb.DateTimeProperty(auto_now_add = True)
	last_modified = ndb.DateTimeProperty(auto_now = True)

	@classmethod
	def create(cls, comment, author, post):
		comment = cls(comment=comment, author=author.key, parent=post.key)
		return comment.put()

	def delete(self):
		self.key.delete()

	def update(self, comment):
		self.comment = comment
		return self.put

	@classmethod
	def get_comments(cls, post):
		print "[[[GET COMMENT]]]post.key: %s" % post.key
		comments = cls.query(ancestor=post.key).order(-cls.created).fetch()
		for comment in comments:
			print "comment: %s" % comment
		return comments #cls.query(ancestor=key_parent).order(-cls.created).fetch()

	@classmethod
	def delete_comments(cls, post):
		query = cls.query(ancestor=post.key).order(-cls.created)
		comments = query.fetch(keys_only=True)
		ndb.delete_multi(comments)