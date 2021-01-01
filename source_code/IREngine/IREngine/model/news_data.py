from IREngine import db
import json
from sqlalchemy.dialects.mysql import TEXT


class news_data(db.Model):
    __tablename__ = 'news_data'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    title = db.Column(db.String(255))
    content = db.Column(TEXT)
    source = db.Column(db.String(10))
    collect_time = db.Column(db.DATETIME)
    publish_time = db.Column(db.DATETIME)
    read_counts = db.Column(db.Integer)

    def dict(self):
        news = dict(id=self.id, url=self.url, title=self.title, content=self.content, acq_source=self.source,
                    collect_time=self.collect_time.strftime('%Y-%m-%d %H:%M:%S'),
                    publish_time=self.publish_time.strftime('%Y-%m-%d %H:%M:%S'), read_counts=self.read_counts)
        return news
