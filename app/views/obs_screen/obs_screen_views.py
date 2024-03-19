from flask import Blueprint, render_template, request, redirect, url_for
from flask.views import MethodView
from app.utils.html_operator import HtmlOperator
from app.utils.json_operator import JsonOperator
from app.utils.nalf_matches_scraper import MatchesScraper
from app.models import Competition
from app.forms import AddCompetitionForm
from app.database import add_nalf_competition
from app.database import edit_nalf_competition
from app.schemas import CompetitionSchema

obs_screen_blueprint = Blueprint('obs_screen', __name__)


# class ObsScreenMatchesView(MethodView):
#     def get(self, competition_id, date_from, date_to):
#         _competition = Competition.query.filter_by(id=competition_id).first()
#         _scraper = MatchesScraper(_competition.schedule_link)
#         matches = _scraper.scrape_matches(date_from, date_to)
#         return render_template('obs_screen/matches.html', matches=matches['matches'], division=matches['division'])


class Highlight(MethodView):
    def get(self):
        video_id = request.headers.get('Optional-Header')
        data = {'video_id': video_id}
        content = render_template('obs_screen/highlight.html', data=data)
        return '', 204


class Results(MethodView):
    def get(self):
        competition_id = request.headers.get('Optional-Header')
        _competitions = JsonOperator.get_actual_episode_data('competitions')
        _competition = [competition for competition in _competitions if competition['id'] is int(competition_id)][0]
        # _results = _competition['results']
        data = {
            'results': _competition['results'],
            'competition_name': _competition['name'],
            'title': 'Wyniki'
        }
        content = render_template('obs_screen/results.html', data=data)
        HtmlOperator.save_scene('results', content)
        return '', 204


class Table(MethodView):
    def get(self):
        competition_id = request.headers.get('Optional-Header')
        _competitions = JsonOperator.get_actual_episode_data('competitions')
        _competition = [competition for competition in _competitions if competition['id'] is int(competition_id)][0]
        data = {
            'table': _competition['table'],
            'competition_name': _competition['name'],
            'title': 'Tabela'
        }
        content = render_template('obs_screen/table.html', data=data)
        HtmlOperator.save_scene('table', content)
        return '', 204


class Schedule(MethodView):
    def get(self):
        competition_id = request.headers.get('Optional-Header')
        _competitions = JsonOperator.get_actual_episode_data('competitions')
        _competition = [competition for competition in _competitions if competition['id'] is int(competition_id)][0]
        data = {
            'results': _competition['schedule'],
            'competition_name': _competition['name'],
            'title': 'Terminarz'
        }
        content = render_template('obs_screen/schedule.html', data=data)
        HtmlOperator.save_scene('schedule', content)
        return '', 204


class Strikers(MethodView):
    def get(self):
        competition_id = request.headers.get('Optional-Header')
        _competitions = JsonOperator.get_actual_episode_data('competitions')
        _competition = [competition for competition in _competitions if competition['id'] is int(competition_id)][0]
        data = {
            'strikers': _competition['strikers'],
            'competition_name': _competition['name'],
            'title': 'Najlepsi strzelcy'
        }
        content = render_template('obs_screen/strikers.html', data=data)
        HtmlOperator.save_scene('strikers', content)
        return '', 204


class Assistants(MethodView):
    def get(self):
        competition_id = request.headers.get('Optional-Header')
        _competitions = JsonOperator.get_actual_episode_data('competitions')
        _competition = [competition for competition in _competitions if competition['id'] is int(competition_id)][0]
        data = {
            'assistants': _competition['assistants'],
            'competition_name': _competition['name'],
            'title': 'Najlepsi asystenci'
        }
        content = render_template('obs_screen/assistants.html', data=data)
        HtmlOperator.save_scene('assistants', content)
        return '', 204


class Canadians(MethodView):
    def get(self):
        competition_id = request.headers.get('Optional-Header')
        _competitions = JsonOperator.get_actual_episode_data('competitions')
        _competition = [competition for competition in _competitions if competition['id'] is int(competition_id)][0]
        data = {
            'canadians': _competition['canadians'],
            'competition_name': _competition['name'],
            'title': 'Punkty kanadyjskie'
        }
        content = render_template('obs_screen/canadians.html', data=data)
        HtmlOperator.save_scene('canadians', content)
        return '', 204


class BestFive(MethodView):
    def get(self):
        competition_id = request.headers.get('Optional-Header')
        _competitions = JsonOperator.get_actual_episode_data('competitions')
        _competition = [competition for competition in _competitions if competition['id'] is int(competition_id)][0]
        data = {
            'best_five': _competition['best_five'],
            'competition_name': _competition['name'],
            'title': 'Piątka kolejki'
        }
        content = render_template('obs_screen/best-five.html', data=data)
        HtmlOperator.save_scene('best-five', content)
        return '', 204


class Title(MethodView):
    def get(self):
        _title = JsonOperator.get_actual_episode_data('title')
        _episode_id = JsonOperator.get_actual_episode_data('id')
        data = {
            'title': _title,
            'episode_id': _episode_id,
        }
        content = render_template('obs_screen/title.html', data=data)
        HtmlOperator.save_scene('title', content)
        return '', 204

# obs_screen_matches_view = ObsScreenMatchesView.as_view('index')
# obs_screen_blueprint.add_url_rule('/matches/<competition_id>/<date_from>/<date_to>', view_func=obs_screen_matches_view)

highlight_view = Highlight.as_view('highlight')
obs_screen_blueprint.add_url_rule('/obs_screen/highlight', view_func=highlight_view)

results_view = Results.as_view('results')
obs_screen_blueprint.add_url_rule('/obs_screen/results', view_func=results_view)

table_view = Table.as_view('table')
obs_screen_blueprint.add_url_rule('/obs_screen/table', view_func=table_view)

schedule_view = Schedule.as_view('schedule')
obs_screen_blueprint.add_url_rule('/obs_screen/schedule', view_func=schedule_view)

strikers_view = Strikers.as_view('strikers')
obs_screen_blueprint.add_url_rule('/obs_screen/strikers', view_func=strikers_view)

assistants_view = Assistants.as_view('assistants')
obs_screen_blueprint.add_url_rule('/obs_screen/assistants', view_func=assistants_view)

canadians_view = Canadians.as_view('canadians')
obs_screen_blueprint.add_url_rule('/obs_screen/canadians', view_func=canadians_view)

best_five_view = BestFive.as_view('best_five')
obs_screen_blueprint.add_url_rule('/obs_screen/best-five', view_func=best_five_view)

title_view = Canadians.as_view('title')
obs_screen_blueprint.add_url_rule('/obs_screen/title', view_func=title_view)
