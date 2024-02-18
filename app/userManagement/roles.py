from flask_security import RoleMixin
from app import db

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

def create_roles():
    admin_role = Role(name='admin', description='Admin user of the website')
    viewer_role = Role(name='viewer', description='Can search other users and see their profiles')
    editor_role = Role(name='editor', description='Can edit and delete the content they uploaded in their own user profile')

    db.session.add(admin_role)
    db.session.add(viewer_role)
    db.session.add(editor_role)

    db.session.commit()