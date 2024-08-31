from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    def __init__(self,data):
        self.id = data['id']
        self.profile_pic = data['profile_pic']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.blog = []
        self.comment = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users(profile_pic,first_name,last_name,email,password,created_at) VALUES (%(profile_pic)s,%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW());"
        results = connectToMySQL('Blogscape').query_db(query,data)
        return results

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user["first_name"]) == 0 or len(user["last_name"]) == 0 or len(user["email"]) == 0 or len(user['password']) == 0:
            is_valid = False
            flash("All fields required!")

        if len(user['first_name']) <=0:
            flash(" First Name must be longer than 0 letters!")
            is_valid = False

        if len(user['last_name']) <=0:
            flash("Last Name must be longer than 0 letters!")
            is_valid = False

        if len(user["email"]) >= 0 and not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email format!")
            is_valid = False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters!","register")
            is_valid = False

        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
            is_valid = False

        return is_valid
    
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('Blogscape').query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('Blogscape').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def update_user(cls, data, id):
        query = """UPDATE users SET profile_pic = %(profile_pic)s, first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, updated_at = NOW()
        WHERE id = {};""".format(id)
        results = connectToMySQL('Blogscape').query_db(query,data)
        return results
    
    @classmethod
    def delete_account(cls, user_id):
        query = "DELETE from users WHERE id = %(id)s;"
        data = {
            "id": user_id
        }
        connectToMySQL('Blogscape').query_db(query,data)
        return user_id