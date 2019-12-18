from . import app, db
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from .forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required

from .models import User


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    username = None
    if current_user.is_authenticated:
        username = current_user.name
    title = 'Home'
    insts_id = 3
    return render_template('index.html', title=title, username=username, insts_id=insts_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('已登录')
        flash('ok')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        print(f"有用户登录，用户名：{form.username.data}，密码：{form.password.data}")
        if not user or not user.check_pwd(form.password.data):
            flash('用户名或密码错误！')
            return redirect(url_for('login'))
        # 验证通过，保存登录状态
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            # next_page 未指定 或 指向了一个绝对地址（一般使外部地址），则默认重定向到本站主页
            return redirect(url_for('index'))
        return redirect(url_for(next_page[1:]))  # next_page[1:] 去掉'/'
    return render_template('login.html', form=form, title='登录')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.username.data
        telno = form.telno.data
        pwd = form.password.data
        user = User(name=name, telno=telno, password=pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'用户: {name}, 注册成功')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='注册')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('tip: logout success')
    return redirect(url_for('index'))


@app.route('/test')
@login_required
def test():
    return '已登录，才能显示：hello world'
