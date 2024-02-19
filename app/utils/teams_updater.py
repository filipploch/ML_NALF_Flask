from app.models import Team
from flask import current_app


class TeamsUpdater:
    def __init__(self):
        self.db = current_app.config['DB']

    def update_teams(self, scraped_teams):
        base_list = Team.query.all()
        updated_list = []
        for team in scraped_teams:
            _team = Team.query.filter_by(link=team['link']).first()
            if _team:
                _team.name = team['name']
                _team.logo_file = team['logo_file']
                self._remove_team_from_base_list(base_list, _team)
            else:
                _team = Team(
                    name=team['name'],
                    link=team['link'],
                    logo_file=team['logo_file'],
                    players=[]
                )
            updated_list.append(_team)
            self.db.session.add(_team)
            self.db.session.commit()
        for team in base_list:
            _team = Team.query.filter_by(link=team['link']).first()
            self.db.session.delete(_team)
            self.db.session.commit()


    def _remove_team_from_base_list(self, base_list, _team):
        for team in base_list:
            if team.name == _team.name:
                base_list.remove(team)
