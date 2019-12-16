from flask import redirect, session, render_template, abort

from routes.podcast import podcast_blueprint

from models.podcast import Podcast

from util import user_logged_in


@podcast_blueprint.route("/<int:podcast_id>/delete")
def delete(podcast_id):
    # todo: flashing
    if not user_logged_in():
        abort(401)

    # todo: validate owner or admin, err 403
    try:
        podcast = Podcast.get_from_id(podcast_id)
        podcast.delete()
    except:
        abort(500)

    return redirect("/")
