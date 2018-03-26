from flask import redirect, render_template, request, url_for, Blueprint
from flask_login import current_user, login_required
from flask_wtf.csrf import validate_csrf
from project.messages.models import Message
from project.users.models import User
from project.users.views import ensure_correct_user
from project.messages.forms import MessageForm
from project import db

messages_blueprint = Blueprint(
    'messages', __name__, template_folder='templates')


@messages_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index(id):
    if request.method == 'POST' and current_user.get_id() == str(id):
        form = MessageForm()
        if form.validate():
            new_message = Message(text=form.text.data, user_id=id)
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for('users.show', id=id))
        return render_template('messages/new.html', form=form)
    user = User.query.get(id)
    messages = user.liked_messages.order_by('timestamp desc')
    return render_template('messages/likes.html', user=user, messages=messages)


@messages_blueprint.route('/new')
@login_required
@ensure_correct_user
def new(id):
    return render_template('messages/new.html', form=MessageForm())


@messages_blueprint.route('/<int:message_id>', methods=['GET', 'DELETE'])
def show(id, message_id):
    found_message = Message.query.get(message_id)
    if request.method == b'DELETE' and current_user.id == id:
        token = request.form.get('csrf_token')
        if validate_csrf(token) == None:
            db.session.delete(found_message)
            db.session.commit()
            return redirect(url_for('users.show', id=id))
        return render_template('404.html')
    return render_template('messages/show.html', message=found_message)


@messages_blueprint.route(
    '/<int:message_id>/message', methods=['POST', 'DELETE'])
@login_required
def like(id, message_id):
    token = request.form.get('csrf_token')
    if validate_csrf(token) == None:
        message = Message.query.get(message_id)
        if request.method == 'POST':
            current_user.liked_messages.append(message)
        else:
            current_user.liked_messages.remove(message)
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('messages.index', id=current_user.id))
    return render_template('404.html')