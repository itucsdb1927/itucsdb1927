from flask import redirect, session, render_template, abort

from models.user import User
from routes.podcast import podcast_blueprint

from models.podcast import Podcast
from routes.podcast._forms import PodcastUpdateForm

from util import user_logged_in


@podcast_blueprint.route("/<int:podcast_id>/update", methods=['GET', 'POST'])
def update(podcast_id):
    if not user_logged_in():
        abort(401)

    user = User.get_from_id(session['user_id'])

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

    # initialize form with current values
    form = PodcastUpdateForm(
        genre=podcast.genre,
        description=podcast.description,
        website_url=podcast.website_url,
    )

    if form.validate_on_submit():
        podcast.genre = form.data['genre']
        podcast.description = form.data['description']
        podcast.website_url = form.data['website_url']
        try:
            podcast.save()
            return redirect(f"/podcast/{podcast_id}")
        except:
            abort(500)

    return render_template(
        "podcast/update.html", form=form, current=podcast, page_title="Update Podcast"
    )
