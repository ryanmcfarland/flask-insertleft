from flask import send_from_directory, redirect, current_app
from app.contact import bp


@bp.route('/download/', methods=['GET'])
def cv():
    #return send_from_directory(current_app.config["CV_DIRECTORY"], filename="CV-RyanMcFarland.pdf")
    return send_from_directory(bp.static_folder, filename="CV-RyanMcFarland.pdf")

@bp.route('/email/', methods=['GET'])
def email():
    return redirect('mailto:'+current_app.config['ADMIN'])
