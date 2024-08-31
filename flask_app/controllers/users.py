from flask import render_template, redirect, session, request, flash, url_for, render_template_string
from flask_app import app
from flask_app.models.user import User
from flask_app.models.info import Info
from flask_app.models.blog import Blog
from werkzeug.utils import secure_filename
import os
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_mail import Mail, Message
mail = Mail(app)
import threading


UPLOAD_FOLDER = 'flask_app/static/profile_pics'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(to, subject, template):
    with app.app_context():
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=app.config['MAIL_USERNAME']
        )
        mail.send(msg)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_account')
def new_account():
    return render_template('register.html')

@app.route('/existing_account')
def existing_account():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # User Validation
    if not User.validate_user(request.form):
        return redirect('/new_account')

    #Confirmation Email
    if request.method == 'POST':
        email = request.form['email']
        confirm_url = url_for('confirm_email', token='dummy-token', _external=True)
    html = render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Confirm Your Email</title>
    </head>
    <body>
        <p>Hi!</p>
        <p>Thanks for signing up. Please follow this link to activate your account:</p>
        <p><a href="{{ confirm_url }}">{{ confirm_url }}</a></p>
        <br>
        <p>Cheers!</p>
    </body>
    </html>
    ''', confirm_url=confirm_url)
    subject = 'Confirm Your Email'
    threading.Thread(target=send_email, args=(email, subject, html)).start()

    #Check if Email exist in DB
    user = User.get_by_email({'email': email})
    if user:
        flash("This account already exists!")
        return redirect('/new_account')

    #Saving profile pic + Saving user data
    file = request.files['profile_pic']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = {
            "profile_pic": filename,
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": bcrypt.generate_password_hash(request.form['password'])
        }
        id = User.save(data)
        session['user_id'] = id
        return redirect('/add/information')

@app.route('/confirm_email/<token>')
def confirm_email(token):
    return render_template('token.html')


@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/existing_account')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/existing_account')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/add/information')
def add_information():
    data = {
        'id': session['user_id']
    }
    return render_template("add_info.html", user=User.get_one(data))

@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    all_blogs = Blog.get_all()
    return render_template("dashboard.html",user = User.get_one(data), blogs = all_blogs, info = Info.get_one(data))


@app.route('/profile')
def profile():
    data = {
        'id': session['user_id']
    }
    all_blogs = Blog.get_all()
    return render_template("profile.html", user = User.get_one(data), blogs = all_blogs, info = Info.get_one(data))


@app.route('/edit/information')
def edit_user_info():
    data = {
        'id': session['user_id']
    }
    all_blogs = Blog.get_all()
    return render_template("edit_profile_info.html", user=User.get_one(data), blogs = all_blogs, info = Info.get_one(data))

@app.route('/update/information')
def update_user_info():
    data = {
        'id': session['user_id']
    }
    return render_template("update_info1.html", user=User.get_one(data), info = Info.get_one(data))


@app.route('/update/information2')
def update_user_info2():
    data = {
        'id': session['user_id']
    }
    return render_template("update_info2.html", user=User.get_one(data), info = Info.get_one(data))

@app.route('/update/<users_id>',methods=['POST'])
def update_user_information(users_id):
    if not User.validate_user(request.form):
        return redirect("/update/information")
    
    file = request.files['profile_pic']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = {
            "profile_pic": filename,
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": bcrypt.generate_password_hash(request.form['password'])
        }
        User.update_user(data, users_id)
    return redirect('/update/information2')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/create_blog')
def add():
    data = {
        'id': session['user_id']
    }
    return render_template("create_blog.html", user = User.get_one(data))

@app.route('/edit/<blogs_id>')
def edit(blogs_id):
    data = {
        'id': blogs_id
    }
    one_blog = Blog.get_one(data)
    return render_template("edit_blog.html", blogs = one_blog)

@app.route("/delete_account/<user_id>")
def delete_account(user_id):
    User.delete_account(user_id)
    return redirect("/")

