from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Revision(db.Model):
    __tablename__ = 'revisions'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    post_id = db.Column(UUID(as_uuid=True), db.ForeignKey('posts.id'), nullable=False)
    content = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String, nullable=True)
    video_url = db.Column(db.String, nullable=True)
    link_url = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, post_id, content=None, image_path=None, video_url=None, link_url=None):
        self.post_id = post_id
        self.content = content
        self.image_path = image_path
        self.video_url = video_url
        self.link_url = link_url