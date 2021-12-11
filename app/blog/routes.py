import datetime

from datetime import datetime
from flask import  request, render_template, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from app import db
from app.blog import bp
from app.blog.forms import BlogForm
from app.blog.models import Entry
from app.common.decorators import role_required


@bp.route('/home',  methods=['GET','POST'])
def home():
    page = request.args.get('page', 1, type=int)
    entries = Entry.query.filter_by(published=True).filter(Entry.slug != None).order_by(Entry.created_at.desc()).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
    for entry in entries.items:
        entry.output_md()
    return render_template('blog/home.html', entries=entries)

#>>> end = datetime(year=2021,month=5,day=10)
#>>> e1=Entry.query.filter(Entry.created_at <= end).all()
@bp.route('/<int:id>/', methods=['GET'])
@bp.route('/<int:year>/<int:month>/<int:day>/<slug>/', methods=['GET'])
def post(id=None, year=None, month=None, day=None, slug=None):#
    if id is None:
        entry = Entry.query.filter(Entry.slug == slug).order_by(Entry.created_at.desc()).first()
        entry.output_md()
    else:
        entry = Entry.query.get_or_404(id)
        entry.output_md()   
    return render_template('blog/post.html', entry=entry)

# Better to create an entry in the db and then redirect to edit page?
@bp.route('/create/', methods=['GET'])
@login_required
@role_required(["Admin", "Power"])
def create():
    entry = Entry(user_id=current_user.id)
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('blog.edit', id=entry.id))

@bp.route('/edit/<int:id>/', methods=['GET','POST'])
@login_required
@role_required(["Admin", "Power"])
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
            entry.published=False
            try:
                db.session.add(entry)
                db.session.commit()
            except:
                flash('Sheet was not updated, database error', 'warning')
                return redirect(url_for('blog.edit', id = id))
        else:
            flash('Sheet was not updated, please check inputs', 'warning')
            return redirect(url_for('blog.edit', id = id))    
        return redirect(url_for('blog.preview', id=id))

# Preview a post to see what it looks like when the md is parsed
# decide to whether make it publically accessible or continue to leave hidden
@bp.route('/preview/<int:id>/', methods=['GET','POST'])
@login_required
@role_required(["Admin", "Power"])
def preview(id):
    if request.method == 'GET':
        entry = Entry.query.get_or_404(id)
        entry.output_md()   
        return render_template('blog/preview.html', entry=entry)
    else:
        entry = Entry.query.get_or_404(id)
        if not entry.publish():
            flash("Cannot publish without a title, caption or content", "warning")
            return redirect(url_for('blog.edit', id=id))
        try:
            db.session.add(entry)
            db.session.commit()
        except:
            db.session.rollback()
            flash('Could not publish article')       
        return redirect(url_for('blog.post', id=entry.id))

# create way to edit, delete and publish posts through this page?
@bp.route('/publish/<int:id>/', methods=['POST'])
@login_required
@role_required(["Admin", "Power"])
def publish(id):
    publish = request.form.get('publish', 'False', type=str)
    publish = True if publish == "True" else False
    entry = Entry.query.get_or_404(id)
    if not entry.publish(publish=publish):
        flash("Cannot publish without a title, caption or content", "warning")
        return redirect(request.referrer)
    try:
        db.session.add(entry)
        db.session.commit()
    except:
        db.session.rollback()
        flash('Error with updating article', 'error')
    return redirect(request.referrer)


@bp.route('/delete/<int:id>/', methods=['GET'])
@login_required
@role_required(["Admin", "Power"])
def delete(id):
    entry = Entry.query.get_or_404(id)
    try:
        db.session.delete(entry)
        db.session.commit()
    except:
        flash("Could not delete Post", 'error')
    return redirect(request.referrer)

# create way to edit, delete and publish posts through this page?
@bp.route('/admin/', methods=['GET','POST'])
@login_required
@role_required("Admin")
def admin():
    page = request.args.get('page', 1, type=int)
    entries = Entry.query.order_by(Entry.created_at.desc()).paginate(page,10,False)
    return render_template('blog/admin.html', entries=entries)