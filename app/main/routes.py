import datetime

from datetime import datetime
from flask import  request, render_template, make_response, current_app
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.blog.models import Entry
from app.common.decorators import role_required

import logging

LOG = logging.getLogger(__name__)

## https://www.digitalocean.com/community/tutorials/how-to-use-python-markdown-with-flask-and-sqlite
## https://stackoverflow.com/questions/43634409/switch-chart-js-data-with-button-click

@bp.route('/', methods=['GET','POST'])
@bp.route('/index/',  methods=['GET','POST'])
def index():
    page = request.args.get('page', 1, type=int)
    entries = Entry.query.filter_by(published=True).filter(Entry.slug != None).order_by(Entry.created_at.desc()).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
    for entry in entries.items:
        entry.output_md()
    resp = make_response(render_template('home.html', entries=entries))
    return resp

# create way to edit, delete and publish posts through this page?
@bp.route('/test', methods=['GET','POST'])
def react():
    return render_template('test.html')