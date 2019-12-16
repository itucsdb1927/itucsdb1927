from flask import redirect, session, render_template, abort

from routes.podcast import podcast_blueprint

from models.podcast import Podcast
from routes.podcast._forms import PodcastEditForm

from util import user_logged_in


@podcast_blueprint.route("/<int:podcast_id>/update", methods=['GET', 'POST'])
def update(podcast_id):
    # todo: add permission check

    podcast = None
    try:
        podcast = Podcast.get_from_id(podcast_id)
    except:
        abort(404)

    form = PodcastEditForm()

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
        "podcast/update.html", form=form, current=podcast, page_title="Create Podcast"
    )
