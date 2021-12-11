import re
import markdown

from datetime import datetime
from app import db

## Many-to-many relationship table between tag and entry
attached_tags = db.Table('attached_tags',
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


#https://github.com/eugenkiss/Simblin/blob/master/simblin/models.py
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, default="")
    slug = db.Column(db.String, unique=True)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    caption = db.Column(db.Text, default="")
    content = db.Column(db.Text, default="")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship("Tag", secondary=attached_tags, backref=db.backref('attached_tags', lazy='dynamic'), lazy='dynamic')

    def output_md(self):
        self.content=markdown.markdown(self.content, extensions=['attr_list', 'fenced_code'])
    
    def output_snapshot(self, snapshot):
        self.content="\n".join(self.content.split("\n")[:snapshot])
        
    def gen_slug(self):
        self.slug = re.sub(r'[^\w]+', '-', self.title.lower()).strip('-')
    
    # If False, always set published to False, return True for upstream checks
    # If true, check contents and return False if any fields empty
    # else set columns and return
    def publish(self, publish=True):
        if not publish:
            self.published=publish
            return True
        elif not self.title or not self.caption or not self.content:
            return False
        else:
            self.published=publish
            self.gen_slug()
            self.publish_date = datetime.utcnow()
            return True

    def __repr__(self):
        return '<Entry {}>'.format(self.title)