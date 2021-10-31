from flask import send_from_directory, redirect, current_app, request, render_template, flash
from flask.helpers import url_for
from app.contact import bp
from app.contact.forms import ContactForm
from app.common.utils import verify_recaptcha, send_email 


@bp.route('/download/', methods=['GET'])
def cv():
    #return send_from_directory(current_app.config["CV_DIRECTORY"], filename="CV-RyanMcFarland.pdf")
    return send_from_directory(current_app.config['CV'], "CV-RyanMcFarland.pdf")

@bp.route('/email/', methods=['GET'])
def email():
    return redirect('mailto:'+current_app.config['ADMIN'])

@bp.route('/contact/', methods=['GET', 'POST'])
def contact(): 
    if request.method == 'POST':
        form = ContactForm(request.form)
        recapthca = verify_recaptcha(request.form['g-recaptcha-response'])
        if form.validate() and recapthca:
            send_email('InsertLeft - Contact Me', 
                        sender=current_app.config['ADMIN'], 
                        recipients=[current_app.config['ADMIN']],
                        text_body=create_text(form.name.data, form.email.data, form.message.data))
            flash("Message sent, I'll reach back soon", 'info')
            return redirect(url_for('main.index'))
        elif "name" in form.errors:
            flash("Name Field - "+form.errors['name'][0], 'warn')
        elif "email" in form.errors:
            flash("Email Field - "+form.errors['email'][0], 'warn')
        elif "message" in form.errors:
            flash(form.errors['message'][0], 'warn')
        elif not recapthca:
            flash("Recaptcha could not be verified", 'warn')
        else:
            flash('Form data could not be processed, please try again', 'warn')
    return render_template('contact/contact.html')

def create_text(name, email, message):
    return """
    From: 
    %s <%s>
    Message:
    %s
    """ % (name, email, message)