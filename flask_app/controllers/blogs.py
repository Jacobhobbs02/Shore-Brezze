from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.blog import Blog

@app.route('/add/blog', methods = ['POST'])
def add_post():
    if Blog.validate_blog(request.form):
        Blog.blog_save(request.form)
        print(request.form)
        return redirect('/dashboard')
    print("FAIL")
    return redirect('/create_blog')

@app.route("/edit/<blogs_id>", methods=['POST'])
def update(blogs_id):
    if not Blog.validate_blog(request.form):
        flash("not successful")
        return redirect("/dashboard")
    Blog.update_blog(request.form,blogs_id)
    return redirect("/dashboard")

@app.route("/delete/<blogs_id>")
def delete_blogs(blogs_id):
    Blog.delete_blog(blogs_id)
    return redirect("/dashboard")