from flask import Flask, request, render_template, flash, redirect, url_for, current_app, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import Entry
from app.main import bp
from app.main.forms import BlogForm


import logging

LOG = logging.getLogger(__name__)

## https://www.digitalocean.com/community/tutorials/how-to-use-python-markdown-with-flask-and-sqlite

@bp.route('/', methods=['GET','POST'])
@bp.route('/index/',  methods=['GET','POST'])
@bp.route('/blog/',  methods=['GET','POST'])
def index():
    entrys = Entry.query.all()
    for entry in entrys:
        entry.output_md()
        entry.output_snapshot(current_app.config['BLOG_SNAPSHOT'])    
    return render_template('home.html', title="hello", entrys=entrys)

# https://stackoverflow.com/questions/43634409/switch-chart-js-data-with-button-click

@bp.route('/blog/create/', methods=['GET','POST'])
@login_required
def create():
    if current_user.username != "test":
        flash('You do not have permissions to create an entry', 'warning')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        content = request.form['content']
        if not content:
            flash('Content is required!')
            return redirect(url_for('main.index'))
        Entry = Entry(note=content)
        db.session.add(Entry)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('blog/create.html')

@bp.route('/blog/<int:id>/', methods=['GET'])
def blog_post(id):
    entry = Entry.query.get_or_404(id)
    entry.output_md()   
    return render_template('blog_post.html', title="hello", entry=entry)