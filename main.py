from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Weresloth1!@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text())

    def __init__(self,title,body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blog %r>' % self.title

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def blog():
    post_id = request.args.get('id')
    blogs = []
    if not post_id:
        blogs = Blog.query.all()
        return render_template('blog.html',blogs=blogs)
    else:
        blogs = Blog.query.filter_by(id=post_id).all()
        return render_template('blog.html',blogs=blogs)

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['blog-body']
        blog_post = Blog(title,body)
        db.session.add(blog_post)
        db.session.commit()

        return redirect('/blog?id=' + str(blog_post.id))
    else:
        return render_template('newpost.html')
if __name__=='__main__':
    app.run()