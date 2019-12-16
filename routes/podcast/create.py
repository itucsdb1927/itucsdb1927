from datetime import datetime

from flask import redirect, session, render_template

from routes.podcast import podcast_blueprint
from routes.podcast._forms import PodcastCreateForm

from models.podcast import Podcast

from util import user_logged_in


@podcast_blueprint.route("/create", methods=['GET', 'POST'])
def create():
    if not user_logged_in():
        return redirect("/")

    form = PodcastCreateForm()

    if form.validate_on_submit():
        podcast = Podcast(
            id_=None,
            maintainer=session.get("user_id", None),
            name=form.data['name'],
            genre=form.data['genre'],
            description=form.data['description'],
            website_url=form.data['website_url'],
            date_created=datetime.now(),
        )
        try:
            podcast.save()
        except:
            pass
        # todo: change to podcast view
        return redirect("/")

    return render_template(
        "podcast/create.html", form=form, page_title="Create Podcast"
    )