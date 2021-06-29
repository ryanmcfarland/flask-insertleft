from flask import Response
from app.common import bp


# Route to automtically create a robots.txt page. Dyanmically creates one and we return the response
# maybe this as well? https://stackoverflow.com/questions/14048779/with-flask-how-can-i-serve-robots-txt-and-sitemap-xml-as-static-files
@bp.route('/robots.txt', methods=['GET'])
def robots():
    r = Response(response="User-Agent: *\nDisallow: /\n", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r