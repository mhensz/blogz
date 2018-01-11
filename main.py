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

    def __init__(self,user_name,password):
        self.user_name = user_name
        self.password = password

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

def is_valid_input(user_input):
    return len(user_input) >=3

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog','index']
    if request.endpoint not in allowed_routes and 'user_name' not in session:
        return redirect('/login')

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html',users=users)

@app.route('/blog')
def blog():
    post_id = request.args.get('id')
    user = request.args.get('user')
    blogs = []
    if not post_id and not user:
        blogs = Blog.query.all()
        return render_template('blog.html',blogs=blogs)
    elif post_id:
        blogs = Blog.query.filter_by(id=post_id).all()
        return render_template('blog.html',blogs=blogs)
    elif user:
        blogs = Blog.query.filter_by(owner_id=user).all()
        return render_template('bloguser.html',blogs=blogs)

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['blog-body']
        owner = User.query.filter_by(user_name=session['user_name']).first()

        if title == "" or body == "":
            flash("Title and Body cannot be empty")
            return redirect('/newpost')
        else:
            blog_post = Blog(title,body,owner)
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
        if user and user.password != password:
            flash('Password is incorrect')
            return redirect('/login')
        if user and user.password == password:
            session['user_name'] = user_name
            return redirect('/newpost')
    else:
        return render_template('login.html')
         


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        verify_pw = request.form['verify_pw']
        existing_user = User.query.filter_by(user_name=user_name).first()

        if not password or not user_name or not verify_pw:
            flash('Username and passwords cannot be blank')
            return redirect('/signup')
        if existing_user:
            flash('That username already exists')
            return redirect('/signup')
        if not is_valid_input(user_name):
            flash('Usernames must be 3 or more characters')
            return redirect('/signup')
        if not is_valid_input(password):
            flash('Passwords must be 3 or more characters')
            return redirect('/signup')
        if password != verify_pw:
            flash('Passwords do not match')
            return redirect('/signup')
        new_user = User(user_name, password)
        db.session.add(new_user)
        db.session.commit()
        session['user_name'] = user_name
        return redirect('/newpost')
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['user_name']
    return redirect('/blog')
if __name__=='__main__':
    app.run()