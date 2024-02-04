from flask import render_template, redirect, url_for, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from . import db, create_app
from app.static import Photo


app = create_app()

images = UploadSet('images', IMAGES)

configure_uploads(app, images)

@app.route('/post/create', methods=['GET', 'POST'])
def create_photo():
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		image = images.save(request.files['image'])
		new_photo = Photo(title=title, content=content, image=image) 
		db.session.add(new_photo)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('create_photo.html')
