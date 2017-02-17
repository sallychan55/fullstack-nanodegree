from handlers.blog_handler import BlogHandler
from google.appengine.ext import ndb

class DeletePost(BlogHandler):
    def get(self, post_id):
        if not self.user:
            self.redirect("/login") 

        key = ndb.Key('Post', int(post_id))
        post = key.get()

        if not post:
            self.error(404)
            return self.render("not_found.html")
                
        self.render("deletepost.html", p=post)

    def post(self, post_id):
        if not self.user:
            self.redirect("/login")

        post= ndb.Key('Post', int(post_id)).get()
        post.delete()
        self.render("deletepost.html", p=post, deleted=True) 