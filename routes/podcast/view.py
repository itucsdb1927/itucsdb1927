from flask import redirect, session, render_template, abort

from routes.podcast import podcast_blueprint

from models.podcast import Podcast


@podcast_blueprint.route("/<int:podcast_id>")
def view(podcast_id):
    try:
        podcast = Podcast.get_from_id(podcast_id)
    except:
        abort(404)

    # todo: implement
    abort(501)
