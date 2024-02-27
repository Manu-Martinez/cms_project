from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.static.models import Post
from app import db


post = Blueprint('post', __name__)

@post.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    
    # Fetch the text from the database
    post = Post.query.get_or_404(id)

    # Ensure the current user is the owner of the text
    if post.owner_id != current_user.id:
        flash('You do not have permission to edit this text.')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        # Get the new text from the form data
        new_post = request.form.get('post')

        if new_post:
            # Update the text record
            post.post = new_post
            db.session.commit()
            flash('Post updated successfully.')
            return redirect(url_for('posts.display_post', id=post.id))

    return render_template('edit_post.html', post=post)

from app.versionControl.revisions import Revision

@post.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    # Fetch the post from the database
    post = Post.query.get(id)
    # If the form is submitted
    if request.method == 'POST':
        # Create a new revision
        if post.content_type == 'text':
            revision = Revision(post_id=post.id, content=post.content)
        elif post.content_type == 'image':
            revision = Revision(post_id=post.id, image_path=post.image_path)
        elif post.content_type == 'video':
            revision = Revision(post_id=post.id, video_url=post.video_url)
        elif post.content_type == 'link':
            revision = Revision(post_id=post.id, link_url=post.link_url)
        db.session.add(revision)
        # Update the post
        if post.content_type == 'text':
            post.content = request.form['content']
        elif post.content_type == 'image':
            post.image_path = request.form['image_path']
        elif post.content_type == 'video':
            post.video_url = request.form['video_url']
        elif post.content_type == 'link':
            post.link_url = request.form['link_url']
        db.session.commit()