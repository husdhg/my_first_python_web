#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:任向民
# datetime:2019/1/10 9:23
# software: PyCharm

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Integer, Column, String, Text, DateTime, create_engine
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/myblogs'
db = SQLAlchemy(app)

from flaskr.models import Users, Blogs, Comment

def db_init():
    db.create_all()

