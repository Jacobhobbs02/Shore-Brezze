from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Blog:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.likes = data['likes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.comment = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM blogs JOIN users ON blogs.user_id = users.id;"
        results = connectToMySQL('Blogscape').query_db(query)
        all_blogs = []
        for row in results:
            one_blog = cls(row)
            user_info = { 
                "id": row['users.id'], 
                "profile_pic": row['profile_pic'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
          
            user = User(user_info)
            one_blog.user = user
            all_blogs.append(one_blog)
        return all_blogs
    
    @classmethod
    def blog_save(cls, data):
        if not cls.validate_blog(data):
            print("not validated")
            return False
        query = "INSERT into blogs (title,content,likes,user_id,created_at,updated_at) values (%(title)s,%(content)s,0,%(user_id)s,NOW(),NOW());"
        result = connectToMySQL('Blogscape').query_db(query, data)
        return result
    
    @classmethod
    def update_blog(cls, data, id):
        query = """UPDATE blogs SET title = %(title)s,content = %(content)s
        WHERE id = {};""".format(id)
        results = connectToMySQL('Blogscape').query_db(query,data)
        return results

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM blogs WHERE blogs.id = %(id)s;"
        result = connectToMySQL('Blogscape').query_db(query,data)  
        return cls(result[0])

    @classmethod
    def validate_blog(cls, data):
        is_valid = True
        if len(data["title"]) == 0:
            flash("Must have a title.")
            is_valid = False
        if len(data["content"]) == 0:
            flash("Must have content")
            is_valid = False
        return is_valid
    
    @classmethod
    def delete_blog(cls, blogs_id):
        query = "DELETE from blogs WHERE id = %(id)s;"
        data = {
            "id": blogs_id
        }
        connectToMySQL('Blogscape').query_db(query,data)
        return blogs_id
    
    
    