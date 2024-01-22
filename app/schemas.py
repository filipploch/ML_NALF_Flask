from app.main import ma
from app.models import Competition, Player, Team
from flask_marshmallow.fields import fields
from marshmallow_sqlalchemy.fields import Nested


class CompetitionSchema(ma.Schema):
    class Meta:
        model = Competition
    id = fields.Int()
    name = fields.Str()
    schedule_link = fields.Str()
    table_link = fields.Str()
    strikers_link = fields.Str()
    assistants_link = fields.Str()
    canadians_link = fields.Str()


nalf_competition_schema = CompetitionSchema()
nalf_competitions_schema = CompetitionSchema(many=True)


class PlayerSchema(ma.Schema):
    class Meta:
        model = Player
    id = fields.Int()
    name = fields.Str()
    team = fields.Int()
    position = fields.Str()
    matches = fields.Int()
    goals = fields.Int()
    assists = fields.Int()
    yellow_cards = fields.Int()
    red_cards = fields.Int()
    own_goals = fields.Int()
    best_five = fields.Int()
    best_player = fields.Int()
    link = fields.Str()


player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)


class TeamSchema(ma.Schema):
    class Meta:
        model = Team
    id = fields.Int()
    name = fields.Str()
    link = fields.Str()
    logo_file = fields.Str()
    players = Nested(players_schema)
