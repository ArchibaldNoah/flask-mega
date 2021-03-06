from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm.attributes import flag_modified

from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    memories = db.relationship('Memory', backref='cerebrum', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    def get_memories(self):
        return Memory.query.filter(Memory.user_id==self.id, Memory.dormant==False).order_by(Memory.timestamp.desc())

    def get_filtered_memories(self, filter_settings):
        if (filter_settings['type']=='Any') & (filter_settings['category']=='Any'):
            current_app.logger.info('Any, Any, {}:'.format(filter_settings['tag_list']))
            if filter_settings['tags']:
                return db.session.query(Memory).join(MemoryTag).join(Tag).filter(Memory.user_id ==self.id, 
                                                                                Memory.dormant==False, 
                                                                                Tag.tag.in_(filter_settings['tag_list'])).order_by(Memory.timestamp.desc())
            else:
                return Memory.query.filter(Memory.user_id==self.id, 
                                        Memory.dormant==False).order_by(Memory.timestamp.desc())
        elif (filter_settings['category']=='Any'):
            return Memory.query.filter(Memory.user_id==self.id, 
                                        Memory.dormant==False, 
                                        Memory.type==str(filter_settings['type'])).order_by(Memory.timestamp.desc())
        else:
            return Memory.query.filter(Memory.user_id==self.id, 
                                        Memory.dormant==False, 
                                        Memory.type==str(filter_settings['type']), 
                                        Memory.category==str(filter_settings['category'])).order_by(Memory.timestamp.desc())

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Memory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    memorized = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(32), index=True)
    category = db.Column(db.String(32), index=True)
    abstract = db.Column(db.String(256))
    tags = db.relationship('Tag', secondary='memory_tag')
    doc = db.Column(JSONB)
    dormant = db.Column(db.Boolean, default=False)

    def get_taglist(self):
        taglist = []
        for item in self.tags:
            taglist.append(item.tag)
        return taglist

    def get_datestring(self):
        return self.timestamp.strftime("%A %Y-%m-%d:%H-%M")

    def get_memory_date(self):
        return self.memorized.strftime("%A %Y-%m-%d:%H-%M")
    
    def set_document(self, value):
        self.doc = value
        flag_modified(self, 'doc')

    def __repr__(self):
        return '<Memory {} of type {}, category {} with {}>'.format(self.id,self.type,self.category,self.doc)

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tag = db.Column(db.String(128), index=True, nullable=False, unique=True)
    tagged_memories = db.relationship('Memory', secondary='memory_tag')


class MemoryTag(db.Model):
    __tablename__ = 'memory_tag'
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    memory_id = db.Column(db.Integer, db.ForeignKey('memory.id'), primary_key=True, autoincrement=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True, autoincrement=False)

