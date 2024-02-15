from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.static.models import Video, Photo, Link
from app import db
from . import multimedia as multimedia_uploadset

multimedia = Blueprint('multimedia', __name__)

@multimedia.route('/edit_multimedia/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_multimedia(id):
    # Fetch the multimedia from the database
    multimedia = Link.query.get_or_404(id)

    # Ensure the current user is the owner of the multimedia
    if multimedia.owner_id != current_user.id:
        flash('You do not have permission to edit this multimedia.')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        # Get the new multimedia file from the form data
        new_multimedia_file = request.files.get('multimedia')

        if new_multimedia_file:
            # Save the new multimedia and update the multimedia record
            new_multimedia_filename = multimedia_uploadset.save(new_multimedia_file)
            multimedia.multimedia = new_multimedia_filename
            db.session.commit()
            flash('Multimedia updated successfully.')
            return redirect(url_for('multimedia.display_multimedia', id=multimedia.id))

    return render_template('edit_multimedia.html', multimedia=multimedia)