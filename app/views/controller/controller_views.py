from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask.views import MethodView
from app.models import NALFcompetition
from app.forms import AddNALFcompetitionForm
from app.database import add_nalf_competition
from app.database import edit_nalf_competition
from app.schemas import NALFcompetitionSchema

controller_blueprint = Blueprint('controller', __name__)


class ControllerIndexView(MethodView):
    def get(self):
        return render_template('controller/index.html')


class ControllerNALFcompetitionsView(MethodView):
    def get(self):
        _competitions = NALFcompetition.query.all()
        return render_template('controller/nalf-competitions.html', competitions=_competitions)


class ControllerAddNALFcompetitionView(MethodView):
    def get(self):
        form = AddNALFcompetitionForm()
        return render_template('controller/add-competition.html', form=form)

    def post(self):
        form = AddNALFcompetitionForm()

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


class ControllerEditNALFcompetitionView(MethodView):
    def get(self, competition_id):
        competition_schema = NALFcompetitionSchema()
        _competition_data = NALFcompetition.query.filter_by(_id=competition_id).first()
        competition_data = competition_schema.dump(_competition_data)
        print(competition_data, flush=True)
        # Utwórz formularz edycji i wypełnij go danymi
        form = AddNALFcompetitionForm(**competition_data)
        return render_template('controller/edit-competition.html', form=form, competition=competition_data)

    def post(self, competition_id):

        form = AddNALFcompetitionForm()

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


controller_view = ControllerIndexView.as_view('index')
controller_blueprint.add_url_rule('/', view_func=controller_view)

competitions_view = ControllerNALFcompetitionsView.as_view('competitions')
controller_blueprint.add_url_rule('/competitions', view_func=competitions_view)

add_competition_view = ControllerAddNALFcompetitionView.as_view('add_competition')
controller_blueprint.add_url_rule('/add-competition', view_func=add_competition_view, methods=['GET', 'POST'])


edit_competition_view = ControllerEditNALFcompetitionView.as_view('edit_competition')
controller_blueprint.add_url_rule('/edit-competition/<int:competition_id>',
                                  view_func=edit_competition_view,
                                  methods=['GET', 'POST'])