from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from .model import Note
from . import db

view = Blueprint('view', __name__)

@view.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if not note or len(note) < 1:
            flash("Note is too short", category='error')
        else:
            new_data = Note(data=note, user_id=current_user.id)
            db.session.add(new_data)
            db.session.commit()
            flash("Note added successfully!", category='success')

    return render_template("index.html", user=current_user)