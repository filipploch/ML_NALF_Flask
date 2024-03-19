from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify, Response, flash
from flask.views import MethodView
from app.models import Competition, Team, Player
from app.forms import AddCompetitionForm
from app.database import add_nalf_competition, edit_nalf_competition, delete_nalf_competition
from app.schemas import CompetitionSchema, players_schema
from app.utils.nalf_table_scraper import TableScraper
from app.utils.nalf_matches_scraper import MatchesScraper
from app.utils.nalf_team_scraper import TeamScraper
from app.utils.title_scraper import TitleScraper
from app.utils.nalf_best_strikers_scraper import StrikersScraper
from app.utils.teams_updater import TeamsUpdater
from app.utils.players_updater import PlayersUpdater
from app.utils.json_operator import JsonOperator
from app.utils.txt_operator import TxtOperator
from app.utils.html_operator import HtmlOperator
from app.utils.date_operator import DateOperator
from app.utils.episode_data_parser import EpisodeDataParser
import json
from datetime import datetime
import threading
from werkzeug.datastructures import ImmutableMultiDict

controller_blueprint = Blueprint('controller', __name__)


class ControllerIndexView(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        _status = obs_ws.get_record_status()
        if _status['outputActive']:
            _record_button_class = 'button-active'
        else:
            _record_button_class = 'button-inactive'
        json_data = JsonOperator.get_json_data('magazines').json
        _editions = json_data['editions']
        actual_edition = [edition for edition in _editions if edition['is_active']][0]
        actual_episode = [episode for episode in actual_edition['episodes'] if episode['is_active']][0]
        actual_episode_id = [episode['id'] for episode in actual_edition['episodes'] if episode['is_active']][0]
        actual_highlights = [highlight for highlight in actual_episode['highlights'] if highlight['is_active']]
        if len(actual_highlights) == 0:
            actual_highlight = [highlight for highlight in actual_episode['highlights']][0]
            actual_highlight_index = 0
        else:
            actual_highlight = actual_highlights[0]
            actual_highlight_index = \
            [index for index, highlight in enumerate(actual_episode['highlights']) if highlight['is_active']][0]
        JsonOperator.set_actual_highlight(actual_highlight_index)
        disabled = ['', '']
        if len(actual_episode['highlights']) < 2:
            disabled[0] = 'disabled'
            disabled[1] = 'disabled'
        elif actual_highlight_index == 0:
            disabled[0] = 'disabled'
        elif actual_highlight_index == len(actual_episode['highlights']) - 1:
            disabled[1] = 'disabled'
        data = {
            'buttonStateClass': _record_button_class,
            'actual_episode': actual_episode,
            'actual_competition': JsonOperator.get_actual_competition(actual_episode_id),
            'disabled': disabled,
            'highlight_idx': actual_highlight_index,
            'actual_highlight': actual_highlight
        }
        return render_template('controller/index.html', data=data, charset='utf-8')


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
        content = render_template('controller/controller-bottom-content.html', audio_icons=_audio_icons,
                                  charset='utf-8')
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
        content = render_template('controller/controller-bottom-content.html', audio_icons=_audio_icons,
                                  charset='utf-8')
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


class ShowSchedule(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.show_schedule()
        return '', 204


class ShowStrikers(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.show_strikers()
        return '', 204


class ShowAssistants(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.show_assistants()
        return '', 204


class ShowCanadians(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.show_canadians()
        return '', 204


class ShowBestFive(MethodView):
    def get(self):
        obs_ws = current_app.config['OBS_WS']
        obs_ws.show_best_five()
        return '', 204


class NalfTeamsUpdater(MethodView):
    def get(self):
        with current_app.app_context():
            self._update_db_teams()
            return jsonify({'status': 'OK'})

    def _update_db_teams(self):
        table_scraper = TableScraper()
        updater = TeamsUpdater()
        _links = [competition.table_link for competition in Competition.query.all()]
        _teams = []
        for link in _links:
            if link is not '':
                _teams.extend(table_scraper.scrape_league_table(link))
        updater.update_teams(_teams)


class NalfPlayersUpdater(MethodView):
    def get(self):
        with current_app.app_context():
            self._update_players()
            # thread = threading.Thread(target=self._update_players, args=(current_app.app_context(),), daemon=True)
            # thread.start()
            return jsonify({'status': 'OK'})

    def _update_players(self):
        db_teams = Team.query.all()
        scraper = TeamScraper()
        updater = PlayersUpdater()
        for team in db_teams:
            _players = scraper.scrape_team_players(team.link)
            updater.update_players(_players, team.id)


class SettingsOverlayMain(MethodView):
    def get(self):
        json_data = JsonOperator.get_json_data('magazines').json
        _editions = json_data['editions']
        actual_edition = [edition for edition in _editions if edition['is_active']][0]
        actual_episode = [episode for episode in actual_edition['episodes'] if episode['is_active']][0]
        actual_episode_index = \
        [index for index, episode in enumerate(actual_edition['episodes']) if episode['is_active']][0]
        actual_episode_id = [episode['id'] for episode in actual_edition['episodes'] if episode['is_active']][0]
        disabled = ['', '']
        if actual_episode_index == 0:
            disabled[0] = 'disabled'
        elif actual_episode_index == len(actual_edition['episodes']) - 1:
            disabled[1] = 'disabled'

        data = {
            'episode': actual_episode,
            'episode_idx': actual_episode_index,
            'disabled': disabled,
            'episode_id': actual_episode_id
        }
        content = render_template('controller/settings/main.html', data=data, charset='utf-8')
        return jsonify({'content': content})


class SetActiveEpisode(MethodView):
    def get(self, episode_idx):
        json_data = JsonOperator.get_json_data('magazines').json
        _editions = json_data['editions']
        actual_edition = [edition for edition in _editions if edition['is_active']][0]
        actual_edition_episodes = [episode for episode in actual_edition['episodes']]
        for episode in actual_edition_episodes:
            episode['is_active'] = False
        actual_edition_episodes[int(episode_idx)]['is_active'] = True
        actual_episode_id = [episode['id'] for episode in actual_edition_episodes if episode['is_active']][0]
        JsonOperator.update_actual_edition_episodes(actual_edition_episodes)
        disabled = ['', '']
        if int(episode_idx) == 0:
            disabled[0] = 'disabled'
        elif int(episode_idx) == len(actual_edition_episodes) - 1:
            disabled[1] = 'disabled'
        TxtOperator.write_text(actual_edition_episodes[int(episode_idx)]['highlights'])
        data = {
            'episode': actual_edition_episodes[int(episode_idx)],
            'episode_idx': int(episode_idx),
            'disabled': disabled,
            'episode_id': actual_episode_id,
            'highlights': actual_edition_episodes[int(episode_idx)]['highlights']
        }
        content = render_template('controller/settings/episodes-wrapper.html', data=data, charset='utf-8')
        return jsonify({'content': content})


class SetActiveHighlight(MethodView):
    def get(self, highlight_idx):
        json_data = JsonOperator.get_json_data('magazines').json
        _editions = json_data['editions']
        actual_edition = [edition for edition in _editions if edition['is_active']][0]
        actual_episode = [episode for episode in actual_edition['episodes'] if episode['is_active']][0]
        if int(highlight_idx) < 0:
            highlight_idx = 0
        if int(highlight_idx) > len(actual_edition['episodes']) - 1:
            highlight_idx = len(actual_edition['episodes']) - 1
        actual_highlight = [highlight for highlight in actual_episode['highlights']][int(highlight_idx)]
        actual_episode_id = [episode['id'] for episode in actual_edition['episodes'] if episode['is_active']][0]
        disabled = ['', '']
        if len(actual_episode['highlights']) < 2:
            disabled[0] = 'disabled'
            disabled[1] = 'disabled'
        elif int(highlight_idx) == 0:
            disabled[0] = 'disabled'
        elif int(highlight_idx) == len(actual_episode['highlights']) - 1:
            disabled[1] = 'disabled'

        data = {
            'actual_episode': actual_episode,
            'actual_competition': JsonOperator.get_actual_competition(actual_episode_id),
            'disabled': disabled,
            'highlight_idx': int(highlight_idx),
            'actual_highlight': actual_highlight,
            'video_id': actual_highlight['video_id'],
            'teams': actual_highlight['teams'],
        }
        JsonOperator.set_actual_highlight(highlight_idx)
        HtmlOperator.save_scene('highlight-start',
                                render_template('obs_screen/highlight-start.html', data=data, charset='utf-8'))
        HtmlOperator.save_scene('highlight',
                                render_template('obs_screen/highlight.html', data=data, charset='utf-8'))
        HtmlOperator.save_scene('highlight-overlay',
                                render_template('obs_screen/highlight-overlay.html', data=data, charset='utf-8'))
        HtmlOperator.save_scene('highlight-end',
                                render_template('obs_screen/highlight-end.html', data=data, charset='utf-8'))
        content = render_template('controller/episode-rows-wrapper.html', data=data, charset='utf-8')
        return jsonify({'content': content})


class UpdateEpisodeTitleBuffer(MethodView):
    def post(self):
        data = request.form
        episode_id = data['episodeId']
        title = [data['episode-title-1'], data['episode-title-2']]
        JsonOperator.update_episode_title_buffer(title, episode_id)
        _flash = 'Tytuł zapisano w buforze'
        content = render_template('controller/utils/flash.html', data=_flash, charset='utf-8')
        return jsonify({'content': content})


class UpdateEpisodeTitle(MethodView):
    def post(self):
        data = request.form
        episode_id = data['episodeId']
        title = [data['episode-title-1'], data['episode-title-2']]
        JsonOperator.update_episode_title(title, episode_id)
        _flash = 'Uaktualniono tytuł'
        content = render_template('controller/utils/flash.html', data=_flash, charset='utf-8')
        return jsonify({'content': content})


class UpdateEpisodeBestFiveBuffer(MethodView):
    def post(self):
        data = request.form
        episode_id = data['episodeId']
        best_five = EpisodeDataParser.parse_best_five_form_data(request.form)
        JsonOperator.update_episode_best_five_buffer(best_five, episode_id)
        _flash = 'Zapisano w buforze Piątkę kolejki'
        content = render_template('controller/utils/flash.html', data=_flash, charset='utf-8')
        return jsonify({'content': content})


class UpdateEpisodeBestFive(MethodView):
    def post(self):
        data = request.form
        episode_id = data['episodeId']
        competition_id = data['competitionId']
        best_five = EpisodeDataParser.parse_best_five_form_data(request.form)
        JsonOperator.update_episode_best_five(best_five, episode_id, competition_id)
        _flash = 'Uaktualniono Piątkę kolejki'
        content = render_template('controller/utils/flash.html', data=_flash, charset='utf-8')
        return jsonify({'content': content})


class UpdateEpisodeHighlightsBuffer(MethodView):
    def post(self):
        data = request.form
        episode_id = data['episodeId']
        highlights = EpisodeDataParser.parse_highlights_form_data(request.form)
        JsonOperator.update_episode_highlights_buffer(highlights, episode_id)
        _flash = 'Skróty zapisano w buforze'
        content = render_template('controller/utils/flash.html', data=_flash, charset='utf-8')
        return jsonify({'content': content})


class UpdateEpisodeHighlights(MethodView):
    def post(self):
        data = request.form
        episode_id = data['episodeId']
        highlights = EpisodeDataParser.parse_highlights_form_data(request.form)
        JsonOperator.update_episode_highlights(highlights, episode_id)
        _flash = 'Uaktualniono skróty'
        content = render_template('controller/utils/flash.html', data=_flash, charset='utf-8')
        return jsonify({'content': content})


class SettingsOverlayEditionView(MethodView):
    def get(self):
        _competitions = Competition.query.all()
        sorted_competitions = sorted(_competitions, key=lambda x: x.name)
        data = {
            'competitions': sorted_competitions
        }
        content = render_template('controller/settings/edition.html', data=data, charset='utf-8')
        return jsonify({'content': content})


class SettingsOverlayAddCompetition(MethodView):
    def get(self):
        form = AddCompetitionForm()
        content = render_template('controller/settings/add-competition.html', form=form, charset='utf-8')
        return jsonify({'content': content})

    def post(self):
        form = AddCompetitionForm()

        if form.validate_on_submit():
            name = form.name.data
            schedule_link = form.schedule_link.data
            table_link = form.table_link.data
            strikers_link = form.strikers_link.data
            assistants_link = form.assistants_link.data
            canadians_link = form.canadians_link.data
            is_cup = 1 if form.is_cup.data else 0

            add_nalf_competition(name, schedule_link, table_link, strikers_link, assistants_link, canadians_link,
                                 is_cup)
            competitions = Competition.query.all()
            content = render_template('controller/settings/edition.html', data=competitions, charset='utf-8')
            return jsonify({'content': content})
        content = render_template('controller/settings/add-competition.html', form=form, charset='utf-8')
        return jsonify({'content': content})


class SettingsOverlayEditCompetition(MethodView):
    def get(self, competition_id):
        competition_schema = CompetitionSchema()
        _competition_data = Competition.query.filter_by(id=competition_id).first()
        competition_data = competition_schema.dump(_competition_data)
        form = AddCompetitionForm(**competition_data)
        content = render_template('controller/settings/edit-competition.html',
                                  form=form, competition=competition_data, charset='utf-8')
        return jsonify({'content': content})

    def post(self, competition_id):
        form = AddCompetitionForm()
        if form.validate_on_submit():
            name = form.name.data
            schedule_link = form.schedule_link.data
            strikers_link = form.strikers_link.data
            assistants_link = form.assistants_link.data
            canadians_link = form.canadians_link.data
            table_link = form.table_link.data
            is_cup = form.is_cup.data
            edit_nalf_competition(competition_id, name, schedule_link, strikers_link, assistants_link, canadians_link,
                                  table_link, is_cup)
            content = render_template('controller/settings/edition.html', charset='utf-8')
            return jsonify({'content': content})
        content = render_template('controller/settings/edit-competition.html', form=form, charset='utf-8')
        return jsonify({'content': content})


class SettingsOverlayDeleteCompetition(MethodView):
    def get(self, competition_id):
        delete_nalf_competition(competition_id)
        return '', 204


class SettingsOverlayBestFive(MethodView):
    def get(self, episode_id):
        data = {'episodeId': episode_id}
        content = render_template('controller/settings/best-five.html', data=data, charset='utf-8')
        return jsonify({'content': content, 'function': 'displayOptions'})


class PlayersView(MethodView):
    def get(self):
        query = request.args.get('query', '').lower()
        TxtOperator.write_text(('query:', query))
        _db_players = Player.query.all()
        _db_teams = Team.query.all()
        team_mapping = {team.id: team.name for team in _db_teams}
        TxtOperator.write_text(team_mapping)
        filtered_results = [player for player in _db_players if query in player.name.lower()]
        if len(filtered_results) > 10:
            filtered_results = filtered_results[:10]
        for result in filtered_results:
            result.team = team_mapping.get(result.team, "Unknown Team")
            TxtOperator.write_text(('result.team:', result.team, '; result.name:', result.name))
        return players_schema.dump(filtered_results)


class SettingsOverlayEditEpisode(MethodView):  # todo
    def get(self, episode_id):
        json_data = JsonOperator.get_json_data('magazines').json
        actual_edition = [edition for edition in json_data['editions'] if edition['is_active']][0]
        episode_to_edit = [episode for episode in actual_edition['episodes'] if episode['id'] is episode_id]
        _competitions = Competition.query.all()
        sorted_competitions = sorted(_competitions, key=lambda x: x.name)
        checked_competitions = [competition for competition in episode_to_edit[0]['competitions']]
        best_five = [competition['best_five'] for competition in episode_to_edit[0]['competitions']
                     if competition['is_cup'] is False][0]
        best_five_data = {
            'is_episode_to_edit': True,
            'best_five': best_five,
            'episode_id': episode_id,
            'competitions': checked_competitions,
        }
        best_five_content = render_template('controller/settings/best-five-buttons-container.html', data=best_five_data)
        highlights = episode_to_edit[0]['highlights']
        title = episode_to_edit[0]['title']
        data = {
            'episode_id': episode_id,
            'edition': actual_edition,
            'episodes': episode_to_edit,
            'competitions': sorted_competitions,
            'checked_competitions': checked_competitions,
            'is_episode_to_edit': True,
            'best_five': best_five_content,
            'highlights': highlights,
            'title': title
        }
        content = render_template('controller/settings/episodes.html', data=data, charset='utf-8')
        return jsonify({'content': content})

    def is_highlights_added(self, highlights):
        if len(highlights) > 0:
            return True
        return False


class SettingsOverlayNewEpisodesSet(MethodView):
    def get(self):
        data = {
            'date_range': [DateOperator.get_last_day_date('tuesday'), DateOperator.get_last_day_date('wednesday'),
                           DateOperator.get_next_day_date('tuesday'), DateOperator.get_next_day_date('wednesday')],
        }
        content = render_template('controller/settings/new-episodes-set.html', data=data, charset='utf-8')
        return jsonify({'content': content})

    def post(self):
        data = request.form
        _competitions = Competition.query.all()
        sorted_competitions = sorted(_competitions, key=lambda x: x.name)
        json_data = JsonOperator.get_json_data('magazines').json
        actual_edition = [edition for edition in json_data['editions'] if edition['is_active']][0]
        last_episode_id = max([int(episode["id"]) for episode in actual_edition["episodes"]])
        this_edition_last_episode_id = max([int(episode["thisEditionEpisodeNumber"])
                                            for episode in actual_edition["episodes"]])
        current_app.config.update({'DATE_RANGE': [data['last-round-start-date'],
                                                  data['last-round-end-date'],
                                                  data['next-round-start-date'],
                                                  data['next-round-end-date']]})
        _new_episodes = []
        for i in range(int(data['new-episodes-number'])):
            _new_episodes.append({'id': last_episode_id + i + 1,
                                  'title': ['', ''],
                                  'date_range': current_app.config['DATE_RANGE'],
                                  'is_active': False,
                                  'thisEditionEpisodeNumber': this_edition_last_episode_id + i + 1,
                                  'highlights': [],
                                  'competitions': []})
        JsonOperator.buffer_new_episodes(_new_episodes)
        _episodes = JsonOperator.get_json_data('buffer-episodes').json

        _data = {
            'episodes': _episodes,
            'last_episode_id': last_episode_id,
            'competitions': sorted_competitions
        }
        content = render_template('controller/settings/episodes.html', data=_data, charset='utf-8')
        return jsonify({'content': content})


class GetTeamsFromSiteTitle(MethodView):
    def get(self, url):
        scraper = TitleScraper()
        _url = f'https://www.youtube.com/watch?v={url}'
        # video_id = self._get_yt_video_id(url)
        title = scraper.scrape_title(_url)['title'].replace(' - YouTube', '')
        if 'Dywizji' in title:
            title = title.split('Dywizji')[1][3:]
        elif 'Pucharu Ligi' in title:
            title = title.split('Pucharu Ligi')[1][1:]
        elif 'Flesz!' in title:
            title = title.split('Flesz!')[1][1:]
        return jsonify({'content': title})

    def _get_yt_video_id(self, url):
        if "youtube.com" in url:
            video_id_start = url.find("v=") + 2
            video_id_end = url.find("&", video_id_start)
            if video_id_end == -1:
                return url[video_id_start:]
            else:
                return url[video_id_start:video_id_end]


class GetCompetitionsData(MethodView):
    def post(self):
        try:
            with current_app.app_context():
                data = request.get_json()
                episode_id = data['episodeId']
                _data = {
                    'competitions': [],
                    'episode_id': episode_id
                }
                TxtOperator.write_text((datetime.now(), {'_data': _data}))
                TxtOperator.write_text((datetime.now(), {'data': data}))
                if data['isEdited'] == '1':
                    date_range = JsonOperator.get_actual_episode_data('date_range')
                else:
                    date_range = current_app.config['DATE_RANGE']

                for key in data:
                    TxtOperator.write_text((datetime.now(), 'key.is_digit()'))
                    TxtOperator.write_text((datetime.now(), key.isdigit()))
                    if key.isdigit():
                        _db_data = self._get_competition_data(key, date_range)
                        TxtOperator.write_text(('db_data: ', _db_data))
                        _data['competitions'].append(_db_data)
                TxtOperator.write_text(_data)
                if data['isEdited'] == '0':
                    self.delete_episode_competitions_buffer_data(episode_id)
                    self.update_episode_competitions_buffer_data(episode_id, _data)
                else:
                    self.update_episode_competitions_data(episode_id, _data)
                content = render_template('controller/settings/best-five-buttons-container.html', data=_data)
                TxtOperator.write_text((datetime.now, {'content': content}))
                return jsonify({'content': content})
        except Exception as e:
            return jsonify({'error': str(e)})

    def _get_competition_data(self, competition_id, date_range):
        competition_data = {}
        competition = Competition.query.filter_by(id=competition_id).first()
        competition_data.update({'id': competition.id})
        competition_data.update({'name': competition.name})
        competition_data.update({'is_cup': False if competition.is_cup is 0 else True})
        competition_data.update({'results': self._get_matches(competition, date_range)})
        competition_data.update({'schedule': self._get_matches(competition, date_range, True)})
        competition_data.update({'table': self._update_table_if_not_cup(competition)})
        competition_data.update({'strikers': self._get_strikers(competition)})
        competition_data.update({'assistants': self._get_strikers(competition, 'asysty')})
        competition_data.update({'canadians': self._get_strikers(competition, 'punktykanadyjskie')})
        competition_data.update({'best_five': []})
        competition_data.update({'is_active': True})
        return competition_data
        # matches_link = competition.schedule_link
        # table_link = competition.table_link
        # strikers_link = competition.strikers_link
        # assistants_link = competition.assistants_link
        # canadians_link = competition.canadians_link

    def _get_matches(self, competition, date_range, future=False):
        matches_link = competition.schedule_link
        if future:
            _date_range = [date_range[2], date_range[3]]
        else:
            _date_range = [date_range[0], date_range[1]]
        scraper = MatchesScraper()
        return scraper.scrape_matches(_date_range[0], _date_range[1], matches_link)['matches']

    def _get_table(self, competition):
        table_link = competition.table_link
        scraper = TableScraper()
        return scraper.scrape_league_table(table_link)

    def _update_table_if_not_cup(self, competition):
        if not competition.is_cup:
            return self._get_table(competition)

    def _get_strikers(self, competition, _type='gole'):
        link = competition.strikers_link
        if _type is 'punktykanadyjskie':
            link = competition.canadians_link
        elif _type is 'asysty':
            link = competition.assistants_link
        scraper = StrikersScraper()
        return scraper.scrape_best_strikers(link, _type)

    def update_episode_competitions_buffer_data(self, episode_id, data):
        _episodes = JsonOperator.get_json_data('buffer-episodes').json

        for episode in _episodes:
            if int(episode['id']) is int(episode_id):
                episode['competitions'].append(data)
        JsonOperator.update_episode_buffer(_episodes)

    def update_episode_competitions_data(self, episode_id, data):
        JsonOperator.update_episode_competitions(episode_id, data['competitions'])

    def delete_episode_competitions_buffer_data(self, episode_id):
        _episodes = JsonOperator.get_json_data('buffer-episodes').json

        for episode in _episodes:
            if int(episode['id']) is int(episode_id):
                episode['competitions'] = []
        JsonOperator.update_episode_buffer(_episodes)


class AddBufferedEpisodeToMainList(MethodView):
    def get(self, episode_id):
        _buffered_episode = JsonOperator.get_buffered_episode(episode_id)
        JsonOperator.add_episode(_buffered_episode)
        return '', 204


controller_view = ControllerIndexView.as_view('index')
controller_blueprint.add_url_rule('/', view_func=controller_view)

controller_bottom_content_view = ControllerBottomContent.as_view('controller-bottom-content')
controller_blueprint.add_url_rule('/controller-bottom-content', view_func=controller_bottom_content_view)

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

show_schedule_view = ShowSchedule.as_view('show_schedule')
controller_blueprint.add_url_rule('/show-schedule', view_func=show_schedule_view)

show_strikers_view = ShowStrikers.as_view('show_strikers')
controller_blueprint.add_url_rule('/show-strikers', view_func=show_strikers_view)

show_assistants_view = ShowAssistants.as_view('show_assistantse')
controller_blueprint.add_url_rule('/show-assistants', view_func=show_assistants_view)

show_canadians_view = ShowCanadians.as_view('show_canadians')
controller_blueprint.add_url_rule('/show-canadians', view_func=show_canadians_view)

show_best_five_view = ShowBestFive.as_view('show_best-five')
controller_blueprint.add_url_rule('/show-best-five', view_func=show_best_five_view)

teams_updater_view = NalfTeamsUpdater.as_view('teams_updater')
controller_blueprint.add_url_rule('/update-teams', view_func=teams_updater_view)

players_updater_view = NalfPlayersUpdater.as_view('players_updater')
controller_blueprint.add_url_rule('/update-players', view_func=players_updater_view)

settings_overlay_main_view = SettingsOverlayMain.as_view('settings_overlay_main')
controller_blueprint.add_url_rule('/settings-overlay-main', view_func=settings_overlay_main_view)

settings_overlay_edition_view = SettingsOverlayEditionView.as_view('edition')
controller_blueprint.add_url_rule('/settings-overlay-edition', view_func=settings_overlay_edition_view)

settings_overlay_add_competition_view = SettingsOverlayAddCompetition.as_view('settings_overlay_add_competition')
controller_blueprint.add_url_rule('/settings-overlay-add-competition',
                                  view_func=settings_overlay_add_competition_view,
                                  methods=['GET', 'POST'])

settings_overlay_edit_competition_view = SettingsOverlayEditCompetition.as_view('settings_overlay_edit_competition')
controller_blueprint.add_url_rule('/settings-overlay-edit-competition/<int:competition_id>',
                                  view_func=settings_overlay_edit_competition_view,
                                  methods=['GET', 'POST'])

settings_overlay_delete_competition_view = SettingsOverlayDeleteCompetition.as_view(
    'settings_overlay_delete_competition')
controller_blueprint.add_url_rule('/settings-overlay-delete-competition/<int:competition_id>',
                                  view_func=settings_overlay_delete_competition_view)

settings_overlay_best_five_view = SettingsOverlayBestFive.as_view('settings_overlay_best_five')
controller_blueprint.add_url_rule('/best-five/<int:episode_id>', view_func=settings_overlay_best_five_view)

get_players_view = PlayersView.as_view('settings_overlay_get_players')
controller_blueprint.add_url_rule('/get-players', view_func=get_players_view)

get_teams_from_site_title_view = GetTeamsFromSiteTitle.as_view('get_teams_from_site_title')
controller_blueprint.add_url_rule('/get-teams-from-site-title/<url>', view_func=get_teams_from_site_title_view)

settings_overlay_edit_episode_view = SettingsOverlayEditEpisode.as_view('settings_overlay_edit_episode')
controller_blueprint.add_url_rule('/settings-overlay-edit-episode/<int:episode_id>',
                                  view_func=settings_overlay_edit_episode_view)

settings_overlay_new_episodes_set_view = SettingsOverlayNewEpisodesSet.as_view('settings_overlay_new_episodes_set')
controller_blueprint.add_url_rule('/settings-overlay-new-episodes-set',
                                  view_func=settings_overlay_new_episodes_set_view,
                                  methods=['GET', 'POST'])

get_competitions_data_view = GetCompetitionsData.as_view('get_competitions_data')
controller_blueprint.add_url_rule('/get-competitions-data',
                                  view_func=get_competitions_data_view,
                                  methods=['POST'])

set_active_episode_view = SetActiveEpisode.as_view('set_active_episode')
controller_blueprint.add_url_rule('/set-active-episode/<episode_idx>', view_func=set_active_episode_view)

set_active_highlight_view = SetActiveHighlight.as_view('set_active_highlight')
controller_blueprint.add_url_rule('/set-active-highlight/<highlight_idx>', view_func=set_active_highlight_view)

update_episode_title_buffer_view = UpdateEpisodeTitleBuffer.as_view('update_episode_title_buffer')
controller_blueprint.add_url_rule('/update-episode-title-buffer',
                                  view_func=update_episode_title_buffer_view,
                                  methods=['POST'])

update_episode_title_view = UpdateEpisodeTitle.as_view('update_episode_title')
controller_blueprint.add_url_rule('/update-episode-title',
                                  view_func=update_episode_title_view,
                                  methods=['POST'])

update_episode_best_five_buffer_view = UpdateEpisodeBestFiveBuffer.as_view('update_episode_best_five_buffer')
controller_blueprint.add_url_rule('/update-episode-best-five-buffer',
                                  view_func=update_episode_best_five_buffer_view,
                                  methods=['POST'])

update_episode_best_five_view = UpdateEpisodeBestFive.as_view('update_episode_best_five')
controller_blueprint.add_url_rule('/update-episode-best-five',
                                  view_func=update_episode_best_five_view,
                                  methods=['POST'])

update_episode_highlights_buffer_view = UpdateEpisodeHighlightsBuffer.as_view('update_episode_highlights_buffer')
controller_blueprint.add_url_rule('/update-episode-highlights-buffer',
                                  view_func=update_episode_highlights_buffer_view,
                                  methods=['POST'])

update_episode_highlights_view = UpdateEpisodeHighlights.as_view('update_episode_highlights')
controller_blueprint.add_url_rule('/update-episode-highlights',
                                  view_func=update_episode_highlights_view,
                                  methods=['POST'])

add_episode_to_main_list_view = AddBufferedEpisodeToMainList.as_view('add_episode_to_main_list')
controller_blueprint.add_url_rule('/add-episode-to-main-list/<episode_id>', view_func=add_episode_to_main_list_view)

