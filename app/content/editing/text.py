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