from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Info:
    def __init__(self,data):
        self.id = data['id']
        self.birthday = data['birthday']
        self.age = data['age']
        self.gender = data['gender']
        self.pronouns = data['pronouns']
        self.bio = data['bio']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    
    @classmethod
    def save_info(cls, data):
        query = "INSERT into infos (birthday,age,gender,pronouns,bio,user_id,created_at,updated_at) values (%(birthday)s,%(age)s,%(gender)s,%(pronouns)s,%(bio)s,%(user_id)s,NOW(),NOW());"
        result = connectToMySQL('Blogscape').query_db(query, data)
        return result
    
    @classmethod
    def validate_info(cls, data):
        is_valid = True
        if len(data["birthday"]) == 0:
            flash("Must enter birthday")
            is_valid = False
        if len(data["age"]) == 0:
            flash("Must enter age")
            is_valid = False
        if len(data["gender"]) == 0:
            flash("Must enter gender")
            is_valid = False
        if len(data["pronouns"]) == 0:
            flash("Must enter pronouns")
            is_valid = False
        if len(data["bio"]) == 0:
            flash("Must enter bio")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM infos JOIN users ON infos.user_id = users.id;"
        result = connectToMySQL('Blogscape').query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def update_info(cls, data, id):
        query = """UPDATE infos SET birthday = %(birthday)s, age = %(age)s, gender = %(gender)s, pronouns = %(pronouns)s, bio = %(bio)s, user_id = %(user_id)s, updated_at = NOW()
        WHERE id = {};""".format(id)
        results = connectToMySQL('Blogscape').query_db(query,data)
        return results
    