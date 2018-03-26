from flask import redirect, render_template, request, url_for, Blueprint, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf.csrf import validate_csrf
from project.users.models import User
from project.users.forms import UserForm, LoginForm, EditForm
from project import db
from sqlalchemy.exc import IntegrityError
from functools import wraps

users_blueprint = Blueprint('users', __name__, template_folder='templates')


def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get('id') != current_user.id:
            flash({'text': 'Not Authorized', 'status': 'danger'})
            return redirect(url_for('root'))
        return fn(*args, **kwargs)

    return wrapper


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search = request.form.get('q')
        token = request.form.get('csrf_token')
        if validate_csrf(token) == None:
            users = None
            if search is None or search == '':
                users = User.query.order_by(User.username).all()
            else:
                users = User.query.filter(
                    User.username.like('%%%s%%' % search)).order_by(
                        User.username).all()
            return render_template('users/index.html', users=users)
        return render_template('404.html')
    return render_template('users/index.html', users=User.query.all())


@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()
    if request.method == 'POST':
        if form.validate():
            try:
                new_user = User(
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
                if form.image_url.data:
                    new_user.image_url = form.image_url.data
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
            except IntegrityError as e:
                flash({'text': 'Username already taken', 'status': 'danger'})
                return render_template('users/signup.html', form=form)
            return redirect(url_for('root'))
    return render_template('users/signup.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            found_user = User.authenticate(form.username.data,
                                           form.password.data)
            if found_user:
                login_user(found_user)
                flash({
                    'text': f'Hello, {found_user.username}!',
                    'status': 'success'
                })
                return redirect(url_for('root'))
            flash({'text': 'Invalid credentials.', 'status': 'danger'})
            return render_template('users/login.html', form=form)
    return render_template('users/login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash({'text': 'You have successfully logged out.', 'status': 'success'})
    return redirect(url_for('users.login'))


@users_blueprint.route('/<int:id>/edit')
@login_required
@ensure_correct_user
def edit(id):
    user = User.query.get(id)
    form = EditForm(obj=user)
    return render_template('users/edit.html', form=form, user=user)


@users_blueprint.route(
    '/<int:followee_id>/followee', methods=['POST', 'DELETE'])
@login_required
def followee(followee_id):
    token = request.form.get('csrf_token')
    if validate_csrf(token) == None:
        followed = User.query.get(followee_id)
        if request.method == 'POST':
            current_user.following.append(followed)
        else:
            current_user.following.remove(followed)
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('users.following', id=current_user.id))
    return render_template('404.html')


@users_blueprint.route('/<int:id>/following', methods=['GET'])
@login_required
def following(id):
    return render_template('users/following.html', user=User.query.get(id))


@users_blueprint.route('/<int:id>/followers', methods=['GET'])
@login_required
def followers(id):
    return render_template('users/followers.html', user=User.query.get(id))


@users_blueprint.route('/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def show(id):
    found_user = User.query.get(id)
    if (request.method == 'GET' or current_user.is_anonymous
            or current_user.get_id() != str(id)):
        return render_template('users/show.html', user=found_user)
    if request.method == b'PATCH':
        form = EditForm(request.form)
        if form.validate():
            if User.authenticate(found_user.username, form.password.data):
                found_user.username = form.username.data
                found_user.email = form.email.data
                found_user.first_name = form.first_name.data or None
                found_user.last_name = form.last_name.data or None
                found_user.bio = form.bio.data or None
                found_user.location = form.location.data or None
                found_user.image_url = form.image_url.data or None
                found_user.header_image_url = form.header_image_url.data or None
                db.session.add(found_user)
                db.session.commit()
                return redirect(url_for('users.show', id=id))
            flash({
                'text': 'Wrong password, please try again.',
                'status': 'danger'
            })
        return render_template('users/edit.html', form=form, user=found_user)
    if request.method == b'DELETE':
        token = request.form.get('csrf_token')
        if validate_csrf(token) == None:
            db.session.delete(found_user)
            db.session.commit()
            return redirect(url_for('users.signup'))
        return render_template('404.html')