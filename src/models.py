import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table user
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    public_profile = Column(Boolean)
    active_user = Column(Boolean)
    posts = relationship("Post",backref="user")
    comments = relationship("Comment",backref="user")
    def to_dict(self):
        return {
            "user.id":self.id,
            "name":self.name,
        }
    
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    caption = Column(String(250))
    user_id = Column(ForeignKey("user.id"))
    media = relationship("Media",backref="post")
    user = relationship("User",backref="post")
    comments = relationship("Comment",backref="post")


class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    type = Column(Enum("picture","video"))
    url = Column(String(250))
    post_id = Column(Integer,ForeignKey("post.id"))

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'))
    content = Column(String(250))
    post_id = Column(ForeignKey('post.id'))

class Follower(Base):
    __tablename__ = "follower"
    id = Column(Integer, primary_key=True)
    follower_user = Column(ForeignKey('user.id'))
    followed_user = Column(ForeignKey('user.id'))

class Blocked(Base):
    __tablename__ = "blocked"
    id = Column(Integer, primary_key=True)
    blocking_user = Column(ForeignKey('user.id'))
    blocked_user = Column(ForeignKey('user.id'))


    

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
