from flask import abort
from flask_login import current_user, login_required
from .permissions import Permission
from app.static.models import Content
from flask import abort, app

def has_permission(user, permission_name):
	permission = Permission.query.filter_by(name=permission_name).first()
	if permission is None:
		return False

	for role in user.roles:
		if permission in role.permissions:
			return True

	return False

@app.route('/profile/<int:user_id>')
@login_required
def view_profile():
	if not has_permission(current_user, 'viewer_permission'):
		abort(403)
	# Show the profile...

@app.route('/content/<int:content_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_content(content_id):
    content = Content.query.get_or_404(content_id)
    if content.owner_id != current_user.id:
        abort(403)
    editor_permission = Permission.query.filter_by(name='editor_permission').first()
    if editor_permission not in current_user.roles.permissions:
        abort(403)
    # Allow the user to edit the content...