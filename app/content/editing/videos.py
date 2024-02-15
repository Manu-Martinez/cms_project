from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.static.models import Video
from app import db
from . import videos as videos_uploadset

videos = Blueprint('videos', __name__)

@videos.route('/edit_video/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_video(id):
    # Fetch the video from the database
    video = Video.query.get_or_404(id)

    # Ensure the current user is the owner of the video
    if video.owner_id != current_user.id:
        flash('You do not have permission to edit this video.')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        # Get the new video file from the form data
        new_video_file = request.files.get('video')

        if new_video_file:
            # Save the new video and update the video record
            new_video_filename = videos_uploadset.save(new_video_file)
            video.video = new_video_filename
            db.session.commit()
            flash('Video updated successfully.')
            return redirect(url_for('videos.display_video', id=video.id))

    return render_template('edit_video.html', video=video)
