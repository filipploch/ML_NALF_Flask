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
    def get(self):
        _competition = Competition.query.filter_by(name='Dywizja B').first()
        _scraper = MatchesScraper(_competition.schedule_link)
        matches = _scraper.scrape_matches('2024-01-23', '2024-01-24')
        return render_template('obs_screen/matches.html', matches=matches['matches'], division=matches['division'])


obs_screen_matches_view = ObsScreenMatchesView.as_view('index')
obs_screen_blueprint.add_url_rule('/matches', view_func=obs_screen_matches_view)