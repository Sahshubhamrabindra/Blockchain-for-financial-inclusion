from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Reugee(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    uid = db.Column(db.String(80),nullable = False)
    address = db.Column(db.String(80),nullable = False)
    gender  = db.Column(db.String(1),nullable=False)
    email_address = db.Column(db.String(200),nullable=True,unique=True)
    dob = db.Column(db.Date, nullable=False)
    profile = db.Column(db.String(200))

    
class Queries(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reugee_id = db.Column(db.Integer, db.ForeignKey('reugee.id'), nullable=False)
    query_text = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    status = db.Column(db.Enum('open', 'closed', 'pending', name='query_status'), nullable=False)