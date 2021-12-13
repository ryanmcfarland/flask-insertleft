import os

from flask import request, Response, send_from_directory, current_app, redirect, flash, url_for, render_template
from flask_login import login_required
from app.common import bp
from app.common.decorators import role_required
from werkzeug.utils import secure_filename

# Route to automtically create a robots.txt page. Dyanmically creates one and we return the response
# maybe this as well? https://stackoverflow.com/questions/14048779/with-flask-how-can-i-serve-robots-txt-and-sitemap-xml-as-static-files
@bp.route('/robots.txt', methods=['GET'])
def robots():
    r = Response(response="User-Agent: *\nAllow: /\n", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def check_and_create_directory():
    if not os.path.exists(current_app.config['UPLOAD_IMAGES_FOLDER']):
        os.makedirs(current_app.config['UPLOAD_IMAGES_FOLDER'])

@bp.route('/upload/', methods=['GET','POST'])
@login_required
@role_required("Admin")
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            check_and_create_directory()
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_IMAGES_FOLDER'], filename)
            file.save(filepath)
            return redirect(url_for('common.media', name=filename))
    return render_template('common/upload.html')

@bp.route('/media/images/<name>')
def media(name):
    return send_from_directory(current_app.config["UPLOAD_IMAGES_FOLDER"], name)

@bp.route('/media/images')
@login_required
@role_required("Admin")
def images():
    files = os.listdir(current_app.config['UPLOAD_IMAGES_FOLDER'])
    return render_template('common/images.html', files = files)