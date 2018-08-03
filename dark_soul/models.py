'''
use SQLAlcheny to persist website data
'''

from datetime import datetime
from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from dark_soul import db

tags = db.Table('bookmark_tag',
                 db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                 db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id'))
                )

class Bookmark(db.Model):
    '''
    Bookmark store
    '''
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _tags = db.relationship('Tag', secondary=tags,
                            backref=db.backref('bookmarks', lazy='dynamic'))

    @staticmethod
    def newest(num):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    '''
    @property
    def tags(self):
        return ",".join([t.name for t in self._tags])

    @tags.setter
    def tags(self, string):
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(',')]
    '''
    @property
    def tags(self):
        return [t.name for t in self._tags]

    @tags.setter
    def tags(self, value_list):
        self._tags = [Tag.get_or_create(name) for name in value_list]


    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.description, self.url)

class User(db.Model, UserMixin):
    '''
    user store
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String) #store the hash of password instead
                                          #of the plain text as password in plain text is dangerous

    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('Password: write-only field')

    @password.setter
    def password(self, pswd):
        self.password_hash = generate_password_hash(pswd)

    def check_password(self, pswd):
        return check_password_hash(self.password_hash, pswd)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return '<User %r>' % self.username


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

    @staticmethod
    def get_or_create(name):
        try:
            return Tag.query.filter_by(name=name).one()
        except:
            return Tag(name=name)

    @staticmethod
    def all():
        return Tag.query.all()

    def __repr__(self):
        return self.name
