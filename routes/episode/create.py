from datetime import datetime, timedelta

from flask import redirect, session, render_template, abort, request

from models.user import User
from routes.episode import episode_blueprint
from routes.episode._forms import EpisodeForm

from models.podcast import Podcast
from models.episode import Episode

from util import user_logged_in


@episode_blueprint.route("/create", methods=['GET', 'POST'])
def create():
    if not user_logged_in():
        abort(401)

    user = User.get_from_id(session['user_id'])

    # retrieve podcast id
    args = request.args.to_dict()
    podcast_id = args.get("podcast_id", None)
    if podcast_id is None:
        abort(400)

    # check if podcast is real
    podcast = None
    try:
        podcast = Podcast.get_from_id(podcast_id)
    except:
        abort(404)

    has_perm = (user is not None) and (
        user.is_admin or (user.id_ == podcast.maintainer)
    )
    if not has_perm:
        abort(403)

    form = EpisodeForm()

    if form.validate_on_submit():
        episode = Episode(
            id_=None,
            podcast=podcast_id,
            title=form.data['title'],
            date=datetime.now(),
            duration=timedelta(minutes=form.data['duration']),
            summary=form.data['summary'],
            episode_number=form.data['episode_number'],
        )
        try:
            episode.save()
            return redirect(f"/podcast/{podcast.id_}")
        except:
            abort(500)

    return render_template(
        "episode/create.html",
        form=form,
        podcast_id=podcast_id,
        page_title="Create Episode",
    )
