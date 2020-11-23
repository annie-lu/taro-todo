from ... import db

class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, index=True,primary_key=True)
    type = db.Column(db.Text, unique=False, nullable=False)
    health = db.Column(db.Float, index=True)
    points = db.Column(db.Integer, index=True)
    account_id = db.Column(db.Integer,db.ForeignKey('account.id'))

    def __init__(self, type, account_id):
        self.type = type
        self.health = 0
        self.points = 0
        self.account_id = account_id
