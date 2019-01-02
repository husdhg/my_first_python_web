#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:任向民
# datetime:2018/12/29 15:18
# software: PyCharm

import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    # 创建flask实例，__name__为当前Python模块名称
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(     # 应用的缺省配置
        SECRET_KEY='dev', # 是被 Flask 和扩展用于保证数据安全的。在开发过程中， 为了方便可以设置为 'dev' ，但是在发布的时候应当使用一个随机值来 重载它。
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), # SQLite 数据库文件存放在路径。
    )
     #判断是否测试
    if test_config is None: # test_config 也会被传递给工厂，并且会替代实例配置。这样可以实现 测试和开发的配置分离，相互独立。
        # load the instance config, if it exists, when not testing
        # 使用 config.py 中的值来重载缺省配置，如果 config.py 存在的话。 例如，当正式部署的时候，用于设置一个正式的 SECRET_KEY 。
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # 确定instance文件存在
    # ensure the instance folder exists
    try:
        # 确保 app.instance_path 存在， Flask 不会自动 创建实例文件夹，但是必须确保创建这个文件夹，因为 SQLite 数据库文件会被 保存在里面。
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 导入调用数据库函数
    from . import db
    db.init_app(app)

    # 使用 app.register_blueprint() 导入并注册 蓝图。新的代码放在工厂函数的尾部返回应用之前。
    # 注册登录蓝图
    from . import auth
    app.register_blueprint(auth.bp)

    # 使用 app.register_blueprint() 在工厂中 导入和注册蓝图。将新代码放在工厂函数的尾部，返回应用之前。
    # 博客蓝图
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    """
    与验证蓝图不同，博客蓝图没有 url_prefix 。
    因此 index 视图会用于 / ， create 会用于 /create ，以此类推。
    博客是 Flaskr 的主要 功能，因此把博客索引作为主索引是合理的。
    但是，下文的 index 视图的端点会被定义为 blog.index 。一些验证视图 会指定向普通的 index 端点。 
    我们使用 app.add_url_rule() 关联端点名称 'index' 和 / URL ，这样 url_for('index') 或 url_for('blog.index') 都会有效，
    会生成同样的 / URL 。
    在其他应用中，可能会在工厂中给博客蓝图一个 url_prefix 并定义一个独立的 index 视图，类似前文中的 hello 视图。
    在这种情况下 index 和 blog.index 的端点和 URL 会有所不同。
    """

    return app



"""
    Windows 下命令行运行flask：
    set FLASK_APP=flaskr
    set FLASK_ENV=development
    flask run
    初始化数据库文件：
    flask init-db
    Initialized the database.
    会在instance 中出现 flaskr.sqlite 文件
"""