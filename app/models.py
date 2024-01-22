from app.main import db


class Competition(db.Model):
    __tablename__ = 'competitions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    team = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    position = db.Column(db.String)
    matches = db.Column(db.Integer)
    goals = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    yellow_cards = db.Column(db.Integer)
    red_cards = db.Column(db.Integer)
    own_goals = db.Column(db.Integer)
    best_five = db.Column(db.Integer)
    best_player = db.Column(db.Integer)
    link = db.Column(db.String)
    
    def __init__(self, name, team, position, matches,
                 goals, assists, yellow_cards, red_cards,
                 own_goals, best_five, best_player, link):
        self.name = name
        self.team = team
        self.position = position
        self.matches = matches
        self.goals = goals
        self.assists = assists
        self.yellow_cards = yellow_cards
        self.red_cards = red_cards
        self.own_goals = own_goals
        self.best_five = best_five
        self.best_player = best_player
        self.link = link


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    link = db.Column(db.String)
    logo_file = db.Column(db.String)
    players = db.relationship('Player',
                              backref='teams',
                              lazy=True,
                              order_by="[desc(Player.position), Player.name]")
    
    def __init__(self, name, link, logo_file, players):
        self.name = name
        self.link = link
        self.logo_file = logo_file
        self.players = players
