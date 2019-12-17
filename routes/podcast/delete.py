from flask import redirect, session, render_template, abort

from models.user import User
from routes.podcast import podcast_blueprint

from models.podcast import Podcast

from util import user_logged_in


@podcast_blueprint.route("/<int:podcast_id>/delete")
def delete(podcast_id):
    if not user_logged_in():
        abort(401)

    user = User.get_from_id(session['user_id'])

    try:
        podcast = Podcast.get_from_id(podcast_id)
        has_perm = (user is not None) and (
            user.is_admin or (user.id_ == podcast.maintainer)
        )
        if not has_perm:
            abort(403)
        podcast.delete()
    except:
        abort(500)

    return redirect("/")
