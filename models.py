
from app import db
from datetime import datetime
import re

from flask_security import UserMixin, RoleMixin
from sqlalchemy import event
from sqlalchemy.orm import *

#ROLE_USER = 0
#ROLE_ADMIN = 1

def slugify(s):                                             #генерация заголовков
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)

post_tags = db.Table('post_tags',
                     db.Column('post_id',                   #post_it - название колонки
                               db.Integer,
                               db.ForeignKey('post.id')),   #post.id - экземпляр класса post, id - свойство
                     db.Column('tag_id',
                               db.Integer,
                               db.ForeignKey('tag.id'))
                     )
####

authors_join = db.Table('authors_join',
                     db.Column('post_id',                   #post_it - название колонки
                               db.Integer,
                               db.ForeignKey('post.id')),   #post.id - экземпляр класса post, id - свойство
                     db.Column('author_id',
                               db.Integer,
                               db.ForeignKey('user.id'))
                     )

####

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140), nullable=False)
    slug = db.Column(db.String(140), unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    authors = db.relationship('User', secondary=authors_join, lazy='joined',
                              backref=db.backref('posts',
                                                 lazy='dynamic'))


    ####
    tags = db.relationship('Tag', secondary=post_tags,
                           backref= db.backref('posts',
                                               lazy='dynamic'))#определяем тип возвразаемых данных

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args,**kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)                     #генерация заголовков

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)

    # posts = db.relationship('Post', secondary=post_tags,
    #                        backref=db.backref('tag',
    #                                           lazy='dynamic'))

    def __init__(self,*args,**kwargs):
        super(Tag, self).__init__(*args,**kwargs)
        self.generate_slug()

    def __repr__(self):
        return '{}'.format(self.name)

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)



### Flask security
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), default= 2)
                       )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255),nullable=False)
    active = db.Column(db.Boolean())
   #articles = db.relationship('Post', lazy=True, secondary=authors_join, backref=db.backref('author', lazy='dynamic'))

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))

    def __repr__(self):                                 #используется для отладки(можно видеть с консоли)
        return '<User {}>'.format(self.nickname)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(255))
    def __repr__(self):
        return 'Role {0}'.format(self.name)

