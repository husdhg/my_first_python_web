#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:任向民
# datetime:2019/1/7 11:28
# software: PyCharm


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Column, String, Text, DateTime, create_engine
from flaskr.database import db



class Users(db.Model):

    __tablename__ = 'user'

    user_id = Column(String(100), primary_key=True)
    user_name = Column(Text)
    pass_word = Column(Text)
    user_worker = Column(Text)
    user_address = Column(Text)
    user_education = Column(Text)
    user_interest = Column(Text)

    def __repr__(self):
        return '<user_name %r>' % self.user_name



class Blogs(db.Model):

    __tablename__ = 'blogs'

    user_id = Column(String(100))
    blog_id = Column(String(100), primary_key=True)
    blog_type = Column(Text)
    blog_label = Column(Text)
    blog_title = Column(Text)
    blog_content = Column(Text)
    blog_datetime = Column(DateTime)
    last_update_time = Column(DateTime)

    def __repr__(self):
        return '<blog_title %r>' % self.blog_title

class Comment(db.Model):

    __tablename__ = 'comments'

    comment_id = Column(String(100), primary_key=True)
    blog_id = Column(String(100))
    user_id = Column(String(100))
    reply_id = Column(String(100))
    comment_datetime = Column(DateTime)
    comment_content = Column(Text)

    def __repr__(self):
        return '<commend_id %r>' % self.commend_id

