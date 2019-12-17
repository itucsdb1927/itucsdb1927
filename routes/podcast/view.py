from flask import redirect, session, render_template, abort

from routes.podcast import podcast_blueprint

from models.user import User
from models.podcast import Podcast

from util import user_logged_in


@podcast_blueprint.route("/<int:podcast_id>")
def view(podcast_id):
    podcast = None
    try:
        podcast = Podcast.get_from_id(podcast_id)
    except:
        abort(404)

    user = None
    if user_logged_in():
        user = User.get_from_id(session['user_id'])

    has_edit_perm = (user is not None) and (
        user.is_admin or (user.id_ == podcast.maintainer)
    )

    return render_template(
        "podcast/view.html",
        user=user,
        podcast=podcast,
        episodes=podcast.episodes,
        maintainer=podcast.get_maintainer(),
        has_edit_perm=has_edit_perm,
        page_title=podcast.name,
    )
