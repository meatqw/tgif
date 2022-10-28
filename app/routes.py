from app import db, app
from flask import Flask, jsonify, render_template, url_for, request, redirect, flash
from app.models import News, User, load_user, UserAdmin
from flask_login import login_user, login_required, logout_user, current_user

# OTHER FUNCTIONS
def get_user():
    """Get current user"""
    user = User.query.filter_by(id=current_user.get_id()).first()
    return user


# ***************** FAQ ******************
@app.route('/faq', methods=['POST', 'GET'])
@login_required
def faq():
    """Render FAQ page"""

    return render_template('faq.html', active='faq', user=get_user())


# ***************** INDEX ******************
@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    """Render main page"""

    return render_template('index.html', active='index', user=get_user())


# ***************** NEWS-PAGE ******************
@app.route('/news/<string:id>', methods=['POST', 'GET'])
@login_required
def news_page(id):
    """Render NEWS-PAGE page"""

    # news = News.query.filter_by(id=id).first()

    return render_template('news-page.html', active='news-page', user=get_user())


# ***************** NEWS ******************
@app.route('/news', methods=['POST', 'GET'])
@login_required
def news():
    """Render news page"""
    
    news = News.query.all()
    return render_template('news.html', active='news', news=news, user=get_user())


# ***************** WALLETS ******************
@app.route('/wallets', methods=['POST', 'GET'])
@login_required
def wallets():
    """Render wallets page"""

    return render_template('wallets.html', active='wallets', user=get_user())

# ***************** REQUEST ******************
@app.route('/request', methods=['POST', 'GET'])
@login_required
def request_():
    """Render request page"""

    return render_template('request.html', active='request', user=get_user())


# ***************** ENTRY (AUTH) ******************
@app.route('/entry', methods=['POST', 'GET'])
def entry():
    """Render Entry page and User authorization"""
    token = request.form.get('token')

    if token:
        user = User.query.filter_by(token=token).first()

        if user is not None:
            login_user(user)

            next = request.args.get('next')

            if next:
                return redirect(next)
            else:
                return redirect(url_for('index'))
        else:
            flash('Token is not correct')
    else:
        flash('Enter token')

    return render_template('entry.html', active='entry')

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('entry'))


@app.after_request
def redirect_to_signin(response):
    """Redirect user without authorization"""
    if response.status_code == 401:
        return redirect(url_for('entry') + '?next=' + request.url)
    else:
        return response


# ***************** ADMIN AUTH ******************
@app.route('/admin/auth', methods=['POST', 'GET'])
def auth():
    """User authorization"""
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = UserAdmin.query.filter_by(login=login).first()

        if user.password == password and user != None:
            login_user(user)

            next = request.args.get('next')

            if next:
                return redirect(next)
            else:
                return redirect('/admin')
        else:
            flash('Login or password is not correct')
    else:
        flash('Enter login and pass')

    return render_template('admin-auth.html')

@app.route('/admin/logout', methods=['POST', 'GET'])
@login_required
def logout_admin():
    logout_user()
    return redirect(url_for('auth'))


@app.after_request
def redirect_to_signin_admin(response):
    """Redirect user without authorization"""
    if response.status_code == 401:
        return redirect(url_for('auth') + '?next=' + request.url)
    else:
        return response