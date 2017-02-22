import os
import webapp2
import jinja2

from google.appengine.ext import ndb

from comment import Comment
from config import app_config

## TODO: should I config in a separate file to store root_path?
template_dir = os.path.join(app_config['root_dir'], "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)
jinja_env.globals['uri_for'] = webapp2.uri_for

class Post(ndb.Model):
	subject = ndb.StringProperty(required = True)
	content = ndb.TextProperty(required = True)
	author = ndb.KeyProperty(required=True, kind="User")
	likes = ndb.KeyProperty(repeated=True, kind="User")
	created = ndb.DateTimeProperty(auto_now_add = True)
	last_modified = ndb.DateTimeProperty(auto_now = True)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, user):
		self._render_text = self.content.replace('\n', '<br>')
		return self.render_str("post.html", p = self, user = user, comments = self.get_comments())

	def get_comments(self):
		print "likes:" % self.likes
		return Comment.get_comments(self)

	@classmethod
	def create(cls, subject, content, author):
		post = cls(subject=subject, content=content, author=author.key)
		return post.put()

	def update(self, subject, content):
		self.subject = subject
		self.content = content
		return self.put()
	
	def delete(self):
		Comment.delete_comments(self)
		self.key.delete()

	def add_like(self, user):
		self.likes.append(user.key)
		return self.put()

	def remove_like(self, user):
		self.likes.remove(user.key)
		return self.put()		        