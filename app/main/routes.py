from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for, current_app, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import Notes
from app.main import bp

import logging

LOG = logging.getLogger(__name__)

## https://www.digitalocean.com/community/tutorials/how-to-use-python-markdown-with-flask-and-sqlite

@bp.route('/', methods=['GET','POST'])
@bp.route('/index',  methods=['GET','POST'])
@bp.route('/blog',  methods=['GET','POST'])
def index():
    notes = Notes.query.all()
    for note in notes:
        note.output_md()    
    return render_template('home.html', title="hello", notes=notes)

# https://stackoverflow.com/questions/43634409/switch-chart-js-data-with-button-click

@bp.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        content = request.form['content']
        if not content:
            flash('Content is required!')
            return redirect(url_for('index'))
        note = Notes(note=content)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('create.html')