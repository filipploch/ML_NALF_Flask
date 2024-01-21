from app.main import db


class NALFcompetition(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    schedule_link = db.Column(db.String(100), nullable=False)
    table_link = db.Column(db.String(100))
    strikers_link = db.Column(db.String(100), nullable=False)
    assistants_link = db.Column(db.String(100), nullable=False)
    canadians_link = db.Column(db.String(100), nullable=False)

    def __init__(self, name, schedule_link, table_link, strikers_link, assistants_link, canadians_link):
        self.name = name
        self.schedule_link = schedule_link
        self.table_link = table_link
        self.strikers_link = strikers_link
        self.assistants_link = assistants_link
        self.canadians_link = canadians_link
