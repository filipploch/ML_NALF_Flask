from app.models import Player
from flask import current_app

class PlayersUpdater:
    def __init__(self):
        self.db = current_app.config['DB']

    def update_players(self, nalffutsal_players, local_db_team_id):
        start_list = Player.query.filter_by(team=local_db_team_id).all()
        updated_list = []
        for player in nalffutsal_players:
            db_player = Player.query.filter_by(name=player['name']).first()
            if db_player:
                db_player.team = local_db_team_id
                db_player.position = player['is_goalkeeper']
                db_player.matches = player['matches']
                db_player.goals = player['goals']
                db_player.assists = player['assists']
                db_player.yellow_cards = player['yellow_cards']
                db_player.red_cards = player['red_cards']
                db_player.own_goals = player['own_goals']
                db_player.best_five = player['best_five']
                db_player.best_player = player['best_player']
                db_player.link = player['link']
                self._remove_player(start_list, db_player)

            else:
                db_player = Player(
                    name=player['name'],
                    team=local_db_team_id,
                    position=player['is_goalkeeper'],
                    matches=player['matches'],
                    goals=player['goals'],
                    assists=player['assists'],
                    yellow_cards=player['yellow_cards'],
                    red_cards=player['red_cards'],
                    own_goals=player['own_goals'],
                    best_five=player['best_five'],
                    best_player=player['best_player'],
                    link=player['link'],
                )
            updated_list.append(db_player)
            self.db.session.add(db_player)
            self.db.session.commit()
        for player in start_list:
            _player = Player.query.filter_by(id=player.id).first()
            _player.team = None
            self.db.session.add(_player)
            self.db.session.commit()
        return {'players': updated_list, 'to_delete': start_list}

    def _remove_player(self, start_list, db_player):
        for player in start_list:
            if player.name == db_player.name:
                start_list.remove(player)

# app = create_app()
# scraper = TeamScraper('drug-ony')
# nalffutsal_players = scraper.scrape_team_players()
# player_comp = PlayersUpdater(app)
# result = player_comp.compare_players(app, nalffutsal_players, 3)
