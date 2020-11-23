from ... import db
from datetime import datetime as dt

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, index=True,primary_key=True)
    content = db.Column(db.Text, index=True,nullable=False)
    done = db.Column(db.Boolean, index=True,default=False)
    account_id = db.Column(db.Integer,db.ForeignKey('account.id'))
    completed_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
    def __init__(self, content, account_id):
        self.content = content
        self.done = False
        self.account_id = account_id
        self.deleted_at = dt.min


    def __repr__(self):
        return '<Content %s>' % self.content