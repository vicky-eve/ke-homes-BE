from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role = db.Column(db.String(255))
    house= db.relationship('House',backref = 'user',lazy="dynamic")
    landlord= db.relationship('Landlord',backref = 'user',lazy="dynamic")
    agent= db.relationship('Agent',backref = 'user',lazy="dynamic")

    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'

class House(db.Model):
    __tablename__ = 'houses'
    id = db.Column(db.Integer,primary_key = True)
    agent = db.Column(db.String(255))
    landlord = db.Column(db.String(255))
    location = db.Column(db.Text())
    pic_path = db.Column(db.String())
    price = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    landlord= db.relationship('Landlord',backref = 'house',lazy="dynamic")
    agent= db.relationship('Agent',backref = 'house',lazy="dynamic")
    
    def save_house(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'House {self.price}'

class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer,primary_key = True)
    agent_name = db.Column(db.String (255), index=True)
    house_id = db.Column(db.Integer,db.ForeignKey("houses.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_agent(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Agent:{self.agent_name}'
        
class Landlord(db.Model):
    __tablename__ = "landlords"
    id=db.Column(db.Integer,primary_key=True)
    landlord_name= db.Column(db.String(255),index=True)
    house_id = db.Column(db.Integer,db.ForeignKey("houses.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_landlord(self):
        db.session.add(self)
        db.session.commit()

     
    def __repr__(self):
        return f'landlord:{self.landlord_name}'