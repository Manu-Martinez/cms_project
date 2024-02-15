from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.static.models import Photo
from app import db
from . import images as images_uploadset 

images = Blueprint('images', __name__)

@images.route('/edit_image/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_image(id):
    # Fetch the image from the database
    image = Photo.query.get_or_404(id)

    # Ensure the current user is the owner of the image
    if image.owner_id != current_user.id:
        flash('You do not have permission to edit this image.')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        # Get the new image file from the form data
        new_image_file = request.files.get('image')

        if new_image_file:
            # Save the new image and update the image record
            new_image_filename = images_uploadset.save(new_image_file)
            image.image = new_image_filename
            db.session.commit()
            flash('Image updated successfully.')
            return redirect(url_for('images.display_image', id=image.id))

    return render_template('edit_image.html', image=image)