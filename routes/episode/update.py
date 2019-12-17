from datetime import timedelta

from flask import redirect, abort, render_template

from routes.episode import episode_blueprint
from routes.episode._forms import EpisodeForm

from models.episode import Episode

from util import user_logged_in


@episode_blueprint.route("/<int:episode_id>/update", methods=['GET', 'POST'])
def update(episode_id):
    # todo: add permission check

    episode = None
    try:
        episode = Episode.get_from_id(episode_id)
    except:
        abort(404)

    # initialize form with current values
    form = EpisodeForm(
        title=episode.title,
        duration=episode.minutes,
        summary=episode.summary,
        episode_number=episode.episode_number
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
