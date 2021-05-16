import datetime

from datetime import datetime
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
    page = request.args.get('page', 1, type=int)
    entries = Entry.query.filter_by(published=True).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
    for entry in entries.items:
        entry.output_md()
        #entry.output_snapshot(current_app.config['BLOG_SNAPSHOT']) 
    next_url = url_for('main.index', page=entries.next_num) if entries.has_next else None
    prev_url = url_for('main.index', page=entries.prev_num) if entries.has_prev else None
    return render_template('home.html', title="hello", entries=entries.items, next_url=next_url, prev_url=prev_url, page=page, np=entries.next_num, pp=entries.prev_num)

#sheets = Sheet.query.filter_by(user_id=current_user.id).all()
#player_sheets = Sheet.query.filter(Sheet.user_id != current_user.id).paginate(page,9,False)
#next_url = url_for('shootout.so_home', page=player_sheets.next_num) if player_sheets.has_next else None
#prev_url = url_for('shootout.so_home', page=player_sheets.prev_num) if player_sheets.has_prev else None

# https://stackoverflow.com/questions/43634409/switch-chart-js-data-with-button-click

# Better to create an entry in the db and then redirect to edit page?
@bp.route('/blog/create/', methods=['GET'])
@login_required
def create():
    if current_user.username != "test":
        flash('You do not have permissions to create an entry', 'warning')
        return redirect(url_for('main.index'))

    entry = Entry(user_id=current_user.id)
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('main.edit', id=entry.id))

#>>> end = datetime(year=2021,month=5,day=10)
#>>> e1=Entry.query.filter(Entry.created_at <= end).all()
@bp.route('/blog/<int:id>/', methods=['GET'])
@bp.route('/blog/<int:year>/<int:month>/<int:day>/<slug>', methods=['GET'])
def blog(id=None, year=None, month=None, slug=None):#
    if id is None:
        entry = Entry.query.filter(Entry.slug == slug).first()
        entry.output_md()
    else:
        entry = Entry.query.get_or_404(id)
        entry.output_md()   
    return render_template('blog/post.html', entry=entry)

@bp.route('/blog/edit/<int:id>/', methods=['GET','POST'])
@login_required
def edit(id):
    if request.method == 'GET':
        entry = Entry.query.get_or_404(id)
        return render_template('blog/edit.html', entry=entry)
    else:
        entry = Entry.query.get_or_404(id)
        form = BlogForm(request.form)
        if form.validate():
            entry.title=form.title.data
            entry.content=form.content.data
            entry.caption=form.caption.data
            entry.last_update = datetime.utcnow()
            db.session.add(entry)
            db.session.commit()
        else:
            flash('Sheet was not updated, please check inputs', 'warning')
            return redirect(url_for('main.edit', id = id))    
        return redirect(url_for('main.preview', id=id))

# Preview a post to see what it looks like when the md is parsed
# decide to whether make it publically accessible or continue to leave hidden
@bp.route('/blog/preview/<int:id>/', methods=['GET','POST'])
@login_required
def preview(id):
    if request.method == 'GET':
        entry = Entry.query.get_or_404(id)
        entry.output_md()   
        return render_template('blog/preview.html', entry=entry)
    else:
        entry = Entry.query.get_or_404(id)
        entry.published=True
        try:
            db.session.add(entry)
            db.session.commit()
        except:
            db.session.rollback()
            flash('Could not publish article')
        
        return redirect(url_for('main.blog', id=entry.id))
            

# create way to edit, delete and publish posts through this page?
@bp.route('/blog/admin/', methods=['GET'])
@login_required
def admin():
    return render_template('blog/admin.html')
