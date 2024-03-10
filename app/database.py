from app.models import Competition
from app.main import db


def add_nalf_competition(name, schedule_link, table_link, strikers_link, assistants_link, canadians_link, is_cup):
    print('add_nalf_competition', is_cup)
    new_nalf_competition = Competition(name, schedule_link, table_link, strikers_link, assistants_link, canadians_link,
                                       is_cup)
    db.session.add(new_nalf_competition)
    db.session.commit()


def edit_nalf_competition(id, name, schedule_link, table_link, strikers_link, assistants_link, canadians_link, is_cup):
    competition = Competition.query.get(id)

    if competition:
        competition.name = name
        competition.schedule_link = schedule_link
        competition.strikers_link = strikers_link
        competition.assistants_link = assistants_link
        competition.canadians_link = canadians_link
        competition.table_link = table_link
        competition.is_cup = is_cup

        db.session.commit()


def delete_nalf_competition(competition_id):
    competition = Competition.query.filter_by(id=competition_id).first()
    if competition:
        db.session.delete(competition)
        db.session.commit()
