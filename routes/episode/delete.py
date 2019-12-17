from flask import redirect, abort

from routes.episode import episode_blueprint
from models.episode import Episode

from util import user_logged_in


@episode_blueprint.route("/<int:episode_id>/delete")
def delete(episode_id):
    # todo: flashing
    if not user_logged_in():
        abort(401)

    # todo: validate owner or admin, err 403
    try:
        episode = Episode.get_from_id(episode_id)
        episode.delete()
        return redirect(f"/podcast/{episode.podcast}")
    except:
        abort(500)

