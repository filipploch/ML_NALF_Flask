from flask import Blueprint, render_template, redirect, url_for, current_app, jsonify, Response
from flask.views import MethodView
from app.models import Competition, Team, Player
from app.forms import AddCompetitionForm
from app.database import add_nalf_competition, edit_nalf_competition
from app.schemas import CompetitionSchema
from app.utils.nalf_table_scraper import TableScraper
from app.utils.nalf_team_scraper import TeamScraper
from app.utils.teams_updater import TeamsUpdater
from app.utils.players_updater import PlayersUpdater
from time import sleep
import threading

controller_blueprint = Blueprint('controller', __name__)


class ControllerIndexView(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        _status = obs_ws.get_record_status()
        if _status['outputActive']:
            _record_button_class = 'button-active'
        else:
            _record_button_class = 'button-inactive'
        return render_template('controller/index.html', buttonStateClass=_record_button_class)


class ControllerBottomContent(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        _microphone_mute_state = obs_ws.get_audio_source_state('Mikrofon')
        _youtube_mute_state = obs_ws.get_audio_source_state('Skrot_YT')
        _music_mute_state = obs_ws.get_audio_source_state('podklad-muzyka')
        _audio_icons = {}
        if _microphone_mute_state is True:
            _audio_icons.update({'microphone-audio-icon': current_app.config['MIKROFON_MUTED']})
        else:
            _audio_icons.update({'microphone-audio-icon': current_app.config['MIKROFON_UNMUTED']})
        if _youtube_mute_state is True:
            _audio_icons.update({'youtube-audio-icon': current_app.config['SKROT_YT_MUTED']})
        else:
            _audio_icons.update({'youtube-audio-icon': current_app.config['SKROT_YT_UNMUTED']})
        if _music_mute_state is True:
            _audio_icons.update({'music-audio-icon': current_app.config['PODKLAD_MUZYKA_MUTED']})
        else:
            _audio_icons.update({'music-audio-icon': current_app.config['PODKLAD_MUZYKA_UNMUTED']})
        content = render_template('controller/controller-bottom-content.html', audio_icons=_audio_icons)
        return jsonify({'content': content})


class ControllerBottomContentChange(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        _microphone_mute_state = obs_ws.get_audio_source_state('Mikrofon')
        _youtube_mute_state = obs_ws.get_audio_source_state('Skrot_YT')
        _music_mute_state = obs_ws.get_audio_source_state('podklad-muzyka')
        _audio_icons = {}
        if _microphone_mute_state is True:
            _audio_icons.update({'microphone-audio-icon': current_app.config['MIKROFON_MUTED']})
        else:
            _audio_icons.update({'microphone-audio-icon': current_app.config['MIKROFON_UNMUTED']})
        if _youtube_mute_state is True:
            _audio_icons.update({'youtube-audio-icon': current_app.config['SKROT_YT_UNMUTED']})
        else:
            _audio_icons.update({'youtube-audio-icon': current_app.config['SKROT_YT_MUTED']})
        if _music_mute_state is True:
            _audio_icons.update({'music-audio-icon': current_app.config['PODKLAD_MUZYKA_UNMUTED']})
        else:
            _audio_icons.update({'music-audio-icon': current_app.config['PODKLAD_MUZYKA_MUTED']})
        content = render_template('controller/controller-bottom-content.html', audio_icons=_audio_icons)
        return jsonify({'content': content})


class GetRecordStatus(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        _status = obs_ws.get_record_status()
        return jsonify(_status), 200, {'Content-Type': 'application/json'}


class StartRecording(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.start_record_cascade()
        return '', 204


class StopRecording(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.end_record_cascade()
        return '', 204


class ShowHighlight(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.higlight_cascade()
        return '', 204


class ShowFlashHighlight(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.flash_highlight_cascade()
        return '', 204


class EndHighlight(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.end_highlight_cascade()
        return '', 204


class ShowStudio(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.show_studio()
        return '', 204


class ShowResults(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.show_results()
        return '', 204


class ShowTable(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.show_table()
        return '', 204


class ShowTimeline(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.show_timeline()
        return '', 204


class ControllerCompetitionsView(MethodView):
    def get(self):
        _competitions = Competition.query.all()
        return render_template('controller/nalf-competitions.html', competitions=_competitions)


class ControllerAddCompetitionView(MethodView):
    def get(self):
        form = AddCompetitionForm()
        return render_template('controller/add-competition.html', form=form)

    def post(self):
        form = AddCompetitionForm()

        if form.validate_on_submit():
            name = form.name.data
            schedule_link = form.schedule_link.data
            strikers_link = form.strikers_link.data
            assistants_link = form.assistants_link.data
            canadians_link = form.canadians_link.data
            table_link = form.table_link.data

            add_nalf_competition(name, schedule_link, strikers_link, assistants_link, canadians_link, table_link)
            return redirect(url_for('controller.index'))
        return render_template('controller/add-competition.html', form=form)


class ControllerEditCompetitionView(MethodView):
    def get(self, competition_id):
        competition_schema = CompetitionSchema()
        _competition_data = Competition.query.filter_by(id=competition_id).first()
        competition_data = competition_schema.dump(_competition_data)
        form = AddCompetitionForm(**competition_data)
        return render_template('controller/edit-competition.html', form=form, competition=competition_data)

    def post(self, competition_id):

        form = AddCompetitionForm()
        if form.validate_on_submit():
            name = form.name.data
            schedule_link = form.schedule_link.data
            strikers_link = form.strikers_link.data
            assistants_link = form.assistants_link.data
            canadians_link = form.canadians_link.data
            table_link = form.table_link.data
            edit_nalf_competition(competition_id, name, schedule_link, strikers_link, assistants_link, canadians_link,
                                  table_link)
            return redirect(url_for('controller.index'))
        return render_template('controller/edit-competition.html', form=form)


class NalfTeamsUpdater(MethodView):
    def get(self):
        thread = threading.Thread(target=self._update_db_teams, args=(current_app.app_context(),), daemon=True)
        thread.start()
        return '', 204

    def _update_db_teams(self, app_context):
        app_context.push()
        table_scraper = TableScraper()
        updater = TeamsUpdater()
        _links = [competition.table_link for competition in Competition.query.all()]
        _teams = []
        for link in _links:
            _teams.extend(table_scraper.scrape_league_table(link))
        updater.update_teams(_teams)

class NalfPlayersUpdater(MethodView):
    def get(self):
        thread = threading.Thread(target=self._update_players, args=(current_app.app_context(),), daemon=True)
        thread.start()
        return '', 204

    def _update_players(self, app_context):
        app_context.push()
        db_teams = Team.query.all()
        scraper = TeamScraper()
        updater = PlayersUpdater()
        for team in db_teams:
            _players = scraper.scrape_team_players(team.link)
            updater.update_players(_players, team.id)






controller_view = ControllerIndexView.as_view('index')
controller_blueprint.add_url_rule('/', view_func=controller_view)

controller_view = ControllerBottomContent.as_view('controller-bottom-content')
controller_blueprint.add_url_rule('/controller-bottom-content', view_func=controller_view)

competitions_view = ControllerCompetitionsView.as_view('competitions')
controller_blueprint.add_url_rule('/competitions', view_func=competitions_view)

add_competition_view = ControllerAddCompetitionView.as_view('add_competition')
controller_blueprint.add_url_rule('/add-competition', view_func=add_competition_view, methods=['GET', 'POST'])

edit_competition_view = ControllerEditCompetitionView.as_view('edit_competition')
controller_blueprint.add_url_rule('/edit-competition/<int:competition_id>',
                                  view_func=edit_competition_view,
                                  methods=['GET', 'POST'])

get_record_status_view = GetRecordStatus.as_view('get_record_status')
controller_blueprint.add_url_rule('/check-record-status', view_func=get_record_status_view)

start_recording_view = StartRecording.as_view('start_recording')
controller_blueprint.add_url_rule('/start-recording', view_func=start_recording_view)

stop_recording_view = StopRecording.as_view('stop_recording')
controller_blueprint.add_url_rule('/stop-recording', view_func=stop_recording_view)

show_highlight_view = ShowHighlight.as_view('show_highlight')
controller_blueprint.add_url_rule('/show-highlight', view_func=show_highlight_view)

show_flash_highlight_view = ShowFlashHighlight.as_view('show_flash_highlight')
controller_blueprint.add_url_rule('/show-flash-highlight', view_func=show_flash_highlight_view)

end_highlight_view = EndHighlight.as_view('end_highlight')
controller_blueprint.add_url_rule('/end-highlight', view_func=end_highlight_view)

show_studio_view = ShowStudio.as_view('show_studio')
controller_blueprint.add_url_rule('/show-studio', view_func=show_studio_view)

show_results_view = ShowResults.as_view('show_results')
controller_blueprint.add_url_rule('/show-results', view_func=show_results_view)

show_table_view = ShowTable.as_view('show_table')
controller_blueprint.add_url_rule('/show-table', view_func=show_table_view)

show_timeline_view = ShowTimeline.as_view('show_timeline')
controller_blueprint.add_url_rule('/show-timeline', view_func=show_timeline_view)

teams_updater_view = NalfTeamsUpdater.as_view('teams_updater')
controller_blueprint.add_url_rule('/update-teams', view_func=teams_updater_view)

players_updater_view = NalfPlayersUpdater.as_view('players_updater')
controller_blueprint.add_url_rule('/update-players', view_func=players_updater_view)