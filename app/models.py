from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Movie:
    def __init__(self,id,title,overview,poster,vote_average,vote_count,genres,backdrop,collection,budget,homepage,date,languages,status,tag,revenue,f_revenue,f_budget,b_collection,runtime):
        self.id =id
        self.title = title
        self.overview = overview
        self.poster = "https://image.tmdb.org/t/p/w500/" + poster
        self.vote_average = vote_average
        self.vote_count = vote_count
        self.genres = genres
        self.backdrop = "https://image.tmdb.org/t/p/w1280/" + backdrop
        self.collection = collection
        self.budget = budget
        self.homepage = homepage
        self.date = date
        self.languages = languages
        self.status = status
        self.tag = tag
        self.revenue = revenue
        self.f_revenue = f_revenue
        self.f_budget = f_budget
        self.b_collection = b_collection
        self.runtime = runtime

class Genres:
    def __init__(self,id,name):
        self.id = id
        self.name = name
       
class Collection:
    def __init__(self,name,overview,poster,backdrop,parts):
        self.name = name
        self.overview = overview
        self.poster = "https://image.tmdb.org/t/p/w1280/"+poster
        self.backdrop = "https://image.tmdb.org/t/p/w1280/"+backdrop
        self.parts = parts

class Cast:
    def __init__(self,character,name,pic):
        self.character = character
        self.name = name
        self.pic = pic

class Review(db.Model):

    __tablename__ = 'reviews'

    id = db.Column(db.Integer,primary_key = True)
    movie_id = db.Column(db.Integer)
    movie_title = db.Column(db.String)
    image_path = db.Column(db.String)
    movie_review = db.Column(db.String)
    posted = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    
    def save_review(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_reviews(cls,id):
        reviews = Review.query.filter_by(movie_id=id).all()

        return reviews

    # all_reviews = []

    # def __init__(self,movie_id,title,imageurl,review):
    #     self.movie_id = movie_id
    #     self.title = title
    #     self.imageurl = imageurl
    #     self.review = review


    # def save_review(self):
    #     Review.all_reviews.append(self)


    # @classmethod
    # def clear_reviews(cls):
    #     Review.all_reviews.clear()

    # @classmethod
    # def get_reviews(cls,id):

    #     response = []

    #     for review in cls.all_reviews:
    #         if review.movie_id == id:
    #             response.append(review)

    #     return response

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    reviews = db.relationship('Review',backref = 'user',lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'