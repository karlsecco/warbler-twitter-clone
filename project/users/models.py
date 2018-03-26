from project import db, bcrypt
from flask_login import UserMixin
from project.messages.models import Message
from sqlalchemy import UniqueConstraint

FollowersFollowee = db.Table(
    'follows', db.Column('id', db.Integer, primary_key=True),
    db.Column('followee_id', db.Integer,
              db.ForeignKey('users.id', ondelete="cascade")),
    db.Column('follower_id', db.Integer,
              db.ForeignKey('users.id', ondelete="cascade")),
    db.CheckConstraint('follower_id != followee_id', name="no_self_follow"))

UserLikes = db.Table('user_likes', db.Column(
    'id', db.Integer, primary_key=True),
                     db.Column('user_id', db.Integer,
                               db.ForeignKey('users.id', ondelete="cascade")),
                     db.Column('message_id', db.Integer,
                               db.ForeignKey(
                                   'messages.id', ondelete="cascade")),
                     UniqueConstraint('user_id', 'message_id'))


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True)
    username = db.Column(db.Text, unique=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    image_url = db.Column(db.Text)
    header_image_url = db.Column(db.Text)
    bio = db.Column(db.Text)
    location = db.Column(db.Text)
    password = db.Column(db.Text)
    messages = db.relationship('Message', backref='user', lazy='dynamic')
    liked_messages = db.relationship(
        'Message',
        secondary=UserLikes,
        backref=db.backref('users_liked', lazy='dynamic'),
        lazy='dynamic')
    followers = db.relationship(
        'User',
        secondary=FollowersFollowee,
        primaryjoin=(FollowersFollowee.c.follower_id == id),
        secondaryjoin=(FollowersFollowee.c.followee_id == id),
        backref=db.backref('following', lazy='dynamic'),
        lazy='dynamic')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

    def __repr__(self):
        return f"#{self.id}: email: {self.email} - username: {self.username}"

    def is_followed_by(self, user):
        return bool(self.followers.filter_by(id=user.id).first())

    def is_following(self, user):
        return bool(self.following.filter_by(id=user.id).first())

    def does_like(self, message):
        return bool(self.liked_messages.filter_by(id=message.id).first())

    def show_follow(self, user):
        return bool(self.id != user.id)

    @classmethod
    def authenticate(cls, username, password):
        found_user = cls.query.filter_by(username=username).first()
        if found_user:
            is_authenticated = bcrypt.check_password_hash(
                found_user.password, password)
            if is_authenticated:
                return found_user
        return False
