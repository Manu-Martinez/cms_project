from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.static.models import Post, Link, Video, Photo
from flask import abort

draft = Blueprint('draft', __name__)

@draft.route('/drafts', methods=['GET'])
@login_required
def view_drafts():
    # Fetch all draft posts, links, videos, and photos for the current user
    drafts = Post.query.filter_by(user_id=current_user.id, published=False).all()
    draft_links = Link.query.filter_by(user_id=current_user.id, published=False).all()
    draft_videos = Video.query.filter_by(user_id=current_user.id, published=False).all()
    draft_photos = Photo.query.filter_by(user_id=current_user.id, published=False).all()
    return render_template('drafts.html', drafts=drafts, draft_links=draft_links, draft_videos=draft_videos, draft_photos=draft_photos)

@draft.route('/drafts/<string:type>/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_draft(type, id):
    # Fetch the draft post, link, video, or photo
    if type == 'post':
        draft = Post.query.get_or_404(id)
    elif type == 'link':
        draft = Link.query.get_or_404(id)
    elif type == 'video':
        draft = Video.query.get_or_404(id)
    elif type == 'photo':
        draft = Photo.query.get_or_404(id)
    else:
        abort(404)

    # Ensure the draft belongs to the current user
    if draft.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        # Update the draft post, link, video, or photo
        draft.body = request.form['body']
        db.session.commit()
        return redirect(url_for('draft.view_drafts'))

    return render_template('edit_draft.html', draft=draft)

@draft.route('/drafts/<string:type>/<int:id>/publish', methods=['POST'])
@login_required
def publish_draft(type, id):
    # Fetch the draft post, link, video, or photo
    if type == 'post':
        draft = Post.query.get_or_404(id)
    elif type == 'link':
        draft = Link.query.get_or_404(id)
    elif type == 'video':
        draft = Video.query.get_or_404(id)
    elif type == 'photo':
        draft = Photo.query.get_or_404(id)
    else:
        abort(404)

    # Ensure the draft belongs to the current user
    if draft.user_id != current_user.id:
        abort(403)

    # Publish the draft post, link, video, or photo
    draft.published = True
    db.session.commit()
    return redirect(url_for('draft.view_drafts'))