import os
import sys
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    profile_picture = Column(String(200))
    bio = Column(String(500))
    registration_date = Column(DateTime, server_default=func.now())

    # Relationship to Post Model (One-to-Many)
    posts = relationship('Post', back_populates='user')
    # Relationship to Comment Model (One-to-Many)
    comments = relationship('Comment', back_populates='user')
    # Relationship to Follow Model - Followers (One-to-Many)
    followers = relationship('Follow', foreign_keys='Follow.following_id', back_populates='following')
    # Relationship to Follow Model - Following (One-to-Many)
    following = relationship('Follow', foreign_keys='Follow.follower_id', back_populates='followers')
    # Relationship to Like Model (One-to-Many)
    likes = relationship('Like', back_populates='user')
    # Relationship to Media Model (One-to-Many)
    media = relationship('Media', back_populates='user')

class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    image_url = Column(String(200), nullable=False)
    caption = Column(String(1000))
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    post_date = Column(DateTime, server_default=func.now())

    # Relationship to User Model (Many-to-One)
    user = relationship('User', back_populates='posts')
    # Relationship to Comment Model (One-to-Many)
    comments = relationship('Comment', back_populates='post')
    # Relationship to Like Model (One-to-Many)
    likes = relationship('Like', back_populates='post')
    # Relationship to Media Model (One-to-One)
    media = relationship('Media', uselist=False, back_populates='post')

class Comment(Base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    text = Column(String(500), nullable=False)
    comment_date = Column(DateTime, server_default=func.now())

    # Relationship to User Model (Many-to-One)
    user = relationship('User', back_populates='comments')
    # Relationship to Post Model (Many-to-One)
    post = relationship('Post', back_populates='comments')

class Follow(Base):
    __tablename__ = 'follows'
    follow_id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    following_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    follow_date = Column(DateTime, server_default=func.now())

    # Relationships to User Model - Follower (Many-to-One)
    followers = relationship('User', foreign_keys=[follower_id], back_populates='following')
    # Relationships to User Model - Following (Many-to-One)
    following = relationship('User', foreign_keys=[following_id], back_populates='followers')

class Like(Base):
    __tablename__ = 'likes'
    like_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    like_date = Column(DateTime, server_default=func.now())

    # Relationships to User Model (Many-to-One)
    user = relationship('User', back_populates='likes')
    # Relationships to Post Model (Many-to-One)
    post = relationship('Post', back_populates='likes')

class Media(Base):
    __tablename__ = 'media'
    media_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    media_type = Column(String(50), nullable=False)
    media_url = Column(String(200), nullable=False)
    upload_date = Column(DateTime, server_default=func.now())

    # Relationship to User Model (Many-to-One)
    user = relationship('User', back_populates='media')
    # Relationship to Post Model (One-to-One)
    post = relationship('Post', back_populates='media')

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
