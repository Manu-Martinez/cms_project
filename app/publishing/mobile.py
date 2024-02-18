from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.static.models import Post
from app import db

mobile = Blueprint('mobile', __name__)

@mobile.route('/publish/<int:post_id>')
@login_required
def publish_post(post_id):
    # Fetch the post from the database
    post = Post.query.get_or_404(post_id)

    # Ensure the current user is the owner of the post
    if post.owner_id != current_user.id:
        flash('You do not have permission to publish this post.')
        return redirect(url_for('main.home'))

    # Update the post's status to published
    post.status = 'published'
    db.session.commit()

    flash('Post published successfully.')
    return redirect(url_for('main.home'))