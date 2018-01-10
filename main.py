from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Weresloth1!@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,title,body,owner):
        self.title = title
        self.body = body
        self.owner = owner

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
        if title == "" or body == "":
            flash("Title and Body cannot be empty")
            return redirect('/newpost')
        else:
            blog_post = Blog(title,body)
            db.session.add(blog_post)
            db.session.commit()

            return redirect('/blog?id=' + str(blog_post.id))
    else:
        return render_template('newpost.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        user = User.query.filter_by(user_name=user_name).first()

        if not user:
            flash('invalid username')
            return redirect('/login')
        elif user and user.password != password:
            flash('Password is incorrect')
            return redirect('/login')
        elif user and user.password == password:
            session['user_name'] = user_name
            return redirect('/newpost')
    else:
        return render_template('login.html')
         


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    pass
if __name__=='__main__':
    app.run()