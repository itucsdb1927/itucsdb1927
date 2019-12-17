from flask import render_template, request, session

from models.podcast import Podcast
from models.user import User

from routes.root import root_blueprint
from util import user_logged_in


@root_blueprint.route("/search", methods=['GET'])
def search():
    user = None
    if user_logged_in():
        user = User.get_from_id(session['user_id'])

    args = request.args.to_dict()
    q = args.get("q", None)

    results = Podcast.search(q) if q else []

    return render_template("root/search.html", user=user, q=q, results=results, page_title="Search")
