from handlers.blog_handler import BlogHandler
from google.appengine.ext import ndb

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class DeletePost(BlogHandler):
    def get(self, post_id):
        key = ndb.Key('Post', int(post_id))
        post = key.get()

        if not post:
            self.error(404)
            return

        self.render("deletepost.html", p=post)

    def post(self, post_id):
        post= ndb.Key('Post', int(post_id)).get()
        post.delete()
        self.render("deletepost.html", p=post, deleted=True) 