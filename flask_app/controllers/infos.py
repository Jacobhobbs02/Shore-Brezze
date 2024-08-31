from flask import render_template,redirect,session,request, flash, url_for
from flask_app import app
from flask_app.models.info import Info

@app.route('/add/info', methods=['GET', 'POST'])
def add_info():
        if Info.validate_info(request.form):   
            Info.save_info(request.form)
            print(request.form)
            return redirect('/dashboard')
        print("FAIL")
        return redirect('/add/information')

@app.route('/new/<infos_id>',methods=['POST'])
def update_infomation(infos_id):
    if not Info.validate_info(request.form):
        flash("not successful")
        return redirect("/update/information2")
    Info.update_info(request.form, infos_id)
    return redirect("/profile")
