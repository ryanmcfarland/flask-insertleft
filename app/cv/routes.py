from flask import send_from_directory, current_app
from app.cv import bp


@bp.route('/download/', methods=['GET'])
def download():
    #return send_from_directory(current_app.config["CV_DIRECTORY"], filename="CV-RyanMcFarland.pdf")
    return send_from_directory(bp.static_folder, filename="CV-RyanMcFarland.pdf")