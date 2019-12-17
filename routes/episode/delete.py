from flask import redirect, abort, session

from models.podcast import Podcast
from models.user import User
from routes.episode import episode_blueprint
from models.episode import Episode

from util import user_logged_in


@episode_blueprint.route("/<int:episode_id>/delete")
def delete(episode_id):
    if not user_logged_in():
        abort(401)

    user = User.get_from_id(session['user_id'])

    try:
        episode = Episode.get_from_id(episode_id)
        has_perm = (user is not None) and (
            user.is_admin or (user.id_ == episode.get_podcast().maintainer)
        )
        if not has_perm:
            abort(403)
        episode.delete()
        return redirect(f"/podcast/{episode.podcast}")
    except:
        abort(500)
