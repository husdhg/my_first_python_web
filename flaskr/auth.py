#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:任向民
# datetime:2019/1/2 10:43
# software: PyCharm

# 登录注册的蓝图
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.database import db, Users

bp = Blueprint('auth', __name__, url_prefix='/auth')

"""
这里创建了一个名称为 'auth' 的 Blueprint 。和应用对象一样，
蓝图需要知道是在哪里定义的，因此把 __name__ 作为函数的第二个参数。 url_prefix 会添加到所有与该蓝图关联的 URL 前面。
"""

# 注册
# @bp.route 关联了 URL /register 和 register 视图函数。当 Flask 收到一个指向 /auth/register 的请求时就会调用 register 视图并把其返回值作为响应。
@bp.route('/register', methods=('GET', 'POST'))
def register():
    # 如果用户提交了表单，那么 request.method 将会是 'POST' 。这咱情况下 会开始验证用户的输入内容。
    if request.method == 'POST':
        # request.form 是一个特殊类型的 dict ，其映射了提交表单的键和值。
        # 表单中，用户将会输入其 username 和 password 。
        user_id = request.form['user_id']
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        worker = request.form['worker']
        education = request.form['education']
        interest = request.form['interest']
        error = None
        # 验证 username 和 password 不为空。
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # 通过查询数据库，检查是否有查询结果返回来验证 username 是否已被注册。
        # db.execute 使用了带有 ? 占位符 的 SQL 查询语句。
        # 占位符可以代替后面的元组参数中相应的值。
        # 使用占位符的 好处是会自动帮你转义输入值，以抵御 SQL 注入攻击 。
        elif Users.query.filter_by(user_id=user_id).first() is not None:
            error = 'User {} is already registered.'.format(username)

        # 如果验证成功，那么在数据库中插入新用户数据。
        # 为了安全原因，不能把密码明文 储存在数据库中。相代替的，使用 generate_password_hash() 生成安全的哈希值并储存 到数据库中。
        # 查询修改了数据库是的数据后使用 meth:db.commit() <sqlite3.Connection.commit> 保存修改。
        if error is None:
            data = Users(user_id = user_id, user_name = username, pass_word = generate_password_hash(password), user_worker = worker, user_address = address,
                         user_education = education, user_interest = interest)
            db.session.add(data)
            db.session.commit()
            # 用户数据保存后将转到登录页面。 url_for() 根据登录视图的名称生成相应的 URL 。
            # 与写固定的 URL 相比， 这样做的好处是如果以后需要修改该视图相应的 URL ，那么不用修改所有涉及到 URL 的代码。
            # redirect() 为生成的 URL 生成一个重定向响应。
            return redirect(url_for('auth.login'))

        # 如果验证失败，那么会向用户显示一个出错信息。 flash() 用于储存在渲染模块时可以调用的信息。
        flash(error)

    # 当用户最初访问 auth/register 时，或者注册出错时，应用显示一个注册 表单。
    # render_template() 会渲染一个包含 HTML 的模板。
    return render_template('auth/register.html')

# 登录
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user_id = request.form['userid']
        password = request.form['password']
        error = None
        user = Users.query.filter_by(user_id=user_id).first()

        if user is None:
            error = 'Incorrect username.'
        # check_password_hash() 以相同的方式哈希提交的 密码并安全的比较哈希值。如果匹配成功，那么密码就是正确的。
        elif not check_password_hash(user.pass_word, password):
            error = 'Incorrect password.'


        # session 是一个 dict ，它用于储存横跨请求的值。当验证 成功后，用户的 id 被储存于一个新的会话中。
        # 会话数据被储存到一个 向浏览器发送的 cookie 中，在后继请求中，浏览器会返回它。
        # Flask 会安全对数据进行 签名 以防数据被篡改。
        if error is None:
            session.clear()
            # 查询用户并存放在变量中，以备后用
            session['user_id'] = user.user_id
            return redirect(url_for('index'))
            # 现在用户的 id 已被储存在 session 中，可以被后续的请求使用。
            # 请每个请求的开头，如果用户已登录，那么其用户信息应当被载入，以使其可用于 其他视图。
        flash(error)

    return render_template('auth/login.html')

# 持续登录
# bp.before_app_request() 注册一个 在视图函数之前运行的函数，不论其 URL 是什么。
# load_logged_in_user 检查用户 id 是否已经储存在 session 中，并从数据库中获取用户数据，然后储存在 g.user 中。
# g.user 的持续时间比请求要长。 如果没有用户 id ，或者 id 不存在，那么 g.user 将会是 None 。
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.filter_by(user_id = user_id).first()

# 注销
# 注销的时候需要把用户 id 从 session 中移除。
# 然后 load_logged_in_user 就不会在后继请求中载入用户了。
@bp.route('/logout')
def logout():
    # 清除 session
    session.clear()
    return redirect(url_for('index'))

# 验证
# 用户登录以后才能创建、编辑和删除博客帖子。在每个视图中可以使用 装饰器 来完成这个工作。
# 装饰器返回一个新的视图，该视图包含了传递给装饰器的原视图。新的函数检查用户 是否已载入。
# 如果已载入，那么就继续正常执行原视图，否则就重定向到登录页面。 我们会在博客视图中使用这个装饰器。
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

# url_for() 函数根据视图名称和发生成 URL 。视图相关联的名称亦称为 端点 ，缺省情况下，端点名称与视图函数名称相同。

# 当使用蓝图的时候，蓝图的名称会添加到函数名称的前面。上面的 login 函数 的端点为 'auth.login' ，因为它已被加入 'auth' 蓝图中。

"""
应用已经写好验证视图，但是如果现在运行服务器的话，无论访问哪个 URL ，都会 看到一个 TemplateNotFound 错误。
这是因为视图调用了 render_template() ，但是模板还没有写。模板文件会储存在 flaskr 包内的 templates 文件夹内。
模板是包含静态数据和动态数据占位符的文件。模板使用指定的数据生成最终的文档。 Flask 使用 Jinja 模板库来渲染模板。
在教程的应用中会使用模板来渲染显示在用户浏览器中的 HTML 。在 Flask 中， Jinja 被配置为 自动转义 HTML 模板中的任何数据。
即渲染用户的输入是安全的。 任何用户输入的可能出现歧意的字符，如 < 和 > ，会被 转义 ，替换为 安全 的值。
这些值在浏览器中看起来一样，但是没有副作用。
Jinja 看上去并且运行地很像 Python 。 
Jinja 语句与模板中的静态数据通过特定的 分界符分隔。 
任何位于 {{ 和 }} 这间的东西是一个会输出到最终文档的静态式。 
{% 和 %} 之间的东西表示流程控制语句，如 if 和 for 。与 Python 不同，代码块使用分界符分隔，而不是使用缩进分隔。
因为代码块内的 静态文本可以会改变缩进。
Flask 自动添加一个 static 视图，视图使用相对于 flaskr/static 的相对路径。
"""