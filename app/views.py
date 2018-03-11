from flask import render_template, flash, redirect, request
from werkzeug.urls import url_parse
from app import app, db
from app.models import User, Song
from app.forms import LoginForm, RegistrationForm


@app.route('/')
@app.route('/index')
def index():
    songs = [
        {
            'artist': 'Bob Dylan',
            'title': 'Blowin\' in the Wind'
        },
        {
            'artist': 'Katie Perry',
            'title': 'I Kissed A Girl'
        }
    ]
    return render_template('index.html',
                           title='All songs',
                           user=user,
                           songs=songs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_autheticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',
                           title='Sign In',
                           form=form
                           )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_autheticated():
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    songs = [
        {
            'artist': 'Bob Dylan',
            'title': 'Blowin in the wind',
            'body': 'The answer is blowin in the wind'
        },
        {
            'artist': 'Katy Perry',
            'title': 'Hot n cold',
            'body': 'You change you mind like a girl changes clothes'
        }
    ]
    return render_template('user.html', user=user, songs=songs)
