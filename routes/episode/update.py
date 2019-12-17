from datetime import timedelta

from flask import redirect, abort, render_template, session

from models.user import User
from routes.episode import episode_blueprint
from routes.episode._forms import EpisodeForm

from models.episode import Episode

from util import user_logged_in


@episode_blueprint.route("/<int:episode_id>/update", methods=['GET', 'POST'])
def update(episode_id):
    if not user_logged_in():
        abort(401)

    user = User.get_from_id(session['user_id'])

    episode = None
    try:
        episode = Episode.get_from_id(episode_id)
    except:
        abort(404)

    has_perm = (user is not None) and (
        user.is_admin or (user.id_ == episode.get_podcast().maintainer)
    )
    if not has_perm:
        abort(403)

    # initialize form with current values
    form = EpisodeForm(
        title=episode.title,
        duration=episode.minutes,
        summary=episode.summary,
        episode_number=episode.episode_number,
    )

    if form.validate_on_submit():
        episode.title = form.data['title']
        episode.duration = timedelta(minutes=form.data['duration'])
        episode.summary = form.data['summary']
        episode.episode_number = form.data['episode_number']
        try:
            episode.save()
            return redirect(f"/podcast/{episode.podcast}")
        except:
            abort(500)

    return render_template(
        "episode/update.html", form=form, page_title="Update Podcast"
    )
