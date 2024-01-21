from app.main import ma
from app.models import NALFcompetition
from flask_marshmallow.fields import fields


class NALFcompetitionSchema(ma.Schema):
    class Meta:
        model = NALFcompetition
    _id = fields.Int()
    name = fields.Str()
    schedule_link = fields.Str()
    table_link = fields.Str()
    strikers_link = fields.Str()
    assistants_link = fields.Str()
    canadians_link = fields.Str()


nalf_competition_schema = NALFcompetitionSchema()
nalf_competitions_schema = NALFcompetitionSchema(many=True)