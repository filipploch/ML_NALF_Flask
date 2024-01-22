from app.models import Competition
from app.main import db


def add_nalf_competition(name, schedule_link, strikers_link, assistants_link, canadians_link, table_link=None):
    new_nalf_competition = Competition(name, schedule_link, table_link, strikers_link, assistants_link, canadians_link)
    db.session.add(new_nalf_competition)
    db.session.commit()


def edit_nalf_competition(id, name, schedule_link, strikers_link, assistants_link, canadians_link, table_link):
    competition = Competition.query.get(id)

    if competition:
        competition.name = name
        competition.schedule_link = schedule_link
        competition.strikers_link = strikers_link
        competition.assistants_link = assistants_link
        competition.canadians_link = canadians_link
        competition.table_link = table_link

        db.session.commit()
