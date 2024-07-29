import requests
import urllib
from time import time
from datetime import datetime
from flask import render_template, redirect, url_for, request, session, Blueprint, jsonify
from flask_login import login_required, logout_user, login_user

from src.views.auth.forms import SignUpForm, SignInForm
from src.models.models import User
from src.extensions import bcrypt
from src.config import Config


auth_bp = Blueprint('auth', __name__)


@auth_bp.before_request
def reset_session_tracks():
    if request.path != '/recommendations':
        if ('tracks' or 'genres_list') in session:
            del session['tracks']
            del session['genres_list']


@auth_bp.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        username_exist = User.query.filter_by(username=form.username.data).all()
        email_exist = User.query.filter_by(email=form.email.data).all()
        if not username_exist and not email_exist:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            user.create()
            return redirect(url_for('auth.sign_in'))
    return render_template('/auth/sign_up.html', form=form)


@auth_bp.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            data = {
                'client_id': Config.CLIENT_ID,
                'client_secret': Config.CLIENT_SECRET,
                'grant_type': 'client_credentials'
            }
            response = requests.post(Config.TOKEN_URL, data=data)
            session['access_token'] = response.json()['access_token']
            session['expire_time'] = datetime.now().timestamp() + response.json()['expires_in']
            login_user(user)
            return redirect(url_for('main.home'))
    return render_template('/auth/sign_in.html', form=form)


# @auth_bp.route('/callback')
# @login_required
# def callback():
#     if 'error' in request.args:
#         return redirect(url_for('main.home'))
#
#     if 'code' in request.args:
#         data = {
#             'code': request.args['code'],
#             'redirect_uri': Config.REDIRECT_URI,
#             'grant_type': 'authorization_code',
#             'content-type': 'application/x-www-form-urlencoded',
#             'client_id': Config.CLIENT_ID,
#             'client_secret': Config.CLIENT_SECRET
#         }
#
#         response = requests.post(Config.TOKEN_URL, data=data)
#         token_info = response.json()
#
#         session['access_token'] = token_info['access_token']
#         session['refresh_token'] = token_info['refresh_token']
#         session['expire_time'] = datetime.now().timestamp() + token_info['expires_in']
#
#         return redirect(url_for('main.home'))
#
#
# @auth_bp.route('/refresh_token')
# @login_required
# def refresh_token():
#     if time() > session['expire_time']:
#         data = {
#             'Content-Type': 'application/x-www-form-urlencoded',
#             'grant_type': 'refresh_token',
#             'refresh_token': session['refresh_token'],
#             'client_id': Config.CLIENT_ID,
#             'client_secret': Config.CLIENT_SECRET
#         }
#
#         response = requests.post('https://accounts.spotify.com/api/token', data=data)
#         token_info = response.json()
#
#         session['access_token'] = token_info['access_token']
#         session['refresh_token'] = token_info['refresh_token']
#
#         return redirect(url_for('main.home'))


@auth_bp.route("/logout")
@login_required
def logout():
    if 'access_token' in session:
        if ('tracks' or 'genres_list') in session:
            del session['tracks']
            del session['genres_list']
        del session['access_token']
        del session['expire_time']
    logout_user()
    return redirect(url_for('main.home'))