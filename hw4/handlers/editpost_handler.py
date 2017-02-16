from handlers.blog_handler import BlogHandler
from google.appengine.ext import ndb

class EditPost(BlogHandler):
    def get(self, post_id):
        post = ndb.Key('Post', int(post_id)).get()
        
        if not post:
            self.error(404)
            return

        self.render("editpost.html", p=post)

    def post(self, post_id):
        subject = self.request.get('subject')
        content = self.request.get('content')
        key_id = self.request.get('key_id')

        post = ndb.Key('Post', int(post_id)).get()

        if not post:
            self.error(404)
            return
                
        if subject and content:
            post.update(subject, content)
            self.render("editpost.html", p=post, updated=True)

        else:
            error = "Please add content!"
            self.render("editpost.html", p=post, subject=subject, content=content, error=error, errors=True)