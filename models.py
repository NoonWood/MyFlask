
from app import db
from datetime import datetime
import re


ROLE_USER = 0
ROLE_ADMIN = 1

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
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now())
   # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))       #внешний ключ
    ####
    authors = db.relationship('User', secondary=authors_join,
                              backref=db.backref('post',
                                                 lazy='dynamic'))
    ####
    tags = db.relationship('Tag', secondary=post_tags,
                           backref= db.backref('post',
                                               lazy='dynamic'))#определяем тип возвразаемых данных

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args,**kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)                     #генерация заголовков

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)



class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    #posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')#использунтся для связи как один

    def __repr__(self):                                 #используется для отладки(можно видеть с консоли)
        return '<User {}>'.format(self.nickname)



class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __init__(self,*args,**kwargs):
        super(Tag, self).__init__(*args,**kwargs)
        self.generate_slug()

    def __repr__(self):
        return '{}'.format(self.name)

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)
'''
def slugify(s):
    return re.sub('[^\w]+','-',s).lower()

class Entry(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)#уникальный заголовок
    body = db.Column(db.Text)
    create_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


    def __init__(self, *args, **kwargs): #устанавливает slug на основе title
        super(Entry, self).__init__(*args,**kwargs)
        self.generate_slag

    def generate_slag(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)

    def __str__(self):
        return 'Entry: %s >' %self.title
'''