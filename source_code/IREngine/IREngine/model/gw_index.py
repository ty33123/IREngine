from IREngine import db
from sqlalchemy.dialects.mysql import MEDIUMTEXT

class GwIndex(db.Model):
    __tablename__ = 'gw_index'
    id = db.Column(db.Integer, primary_key=True)
    publish_org = db.Column(db.String(20))
    issued_word = db.Column(db.String(20))
    issued_year = db.Column(db.Integer)
    issued_num = db.Column(db.Integer)
    foreign_id = db.Column(db.Integer, db.ForeignKey('gw.id'))
    class1 = db.Column(db.String(50))
    class2 = db.Column(db.String(50))
    gw = db.relationship('Gw')
