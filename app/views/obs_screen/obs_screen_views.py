from flask import Blueprint, render_template, redirect, url_for
from flask.views import MethodView
from app.utils.nalf_matches_scraper import MatchesScraper
from app.models import Competition
from app.forms import AddCompetitionForm
from app.database import add_nalf_competition
from app.database import edit_nalf_competition
from app.schemas import CompetitionSchema

obs_screen_blueprint = Blueprint('obs_screen', __name__)


class ObsScreenMatchesView(MethodView):
    def get(self, competition_id, date_from, date_to):
        _competition = Competition.query.filter_by(id=competition_id).first()
        _scraper = MatchesScraper(_competition.schedule_link)
        matches = _scraper.scrape_matches(date_from, date_to)
        return render_template('obs_screen/matches.html', matches=matches['matches'], division=matches['division'])


obs_screen_matches_view = ObsScreenMatchesView.as_view('index')
obs_screen_blueprint.add_url_rule('/matches/<competition_id>/<date_from>/<date_to>', view_func=obs_screen_matches_view)