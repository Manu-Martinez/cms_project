from flask import render_template, redirect, url_for, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, AUDIO, DATA
from . import db, create_app
from app.static import Post, Link, Video, Photo
from . import images, videos


app = create_app()


multimedia = UploadSet('multimedia', AUDIO + DATA)
images = UploadSet('images', IMAGES)
videos = UploadSet('videos', ('mp4', 'avi', 'mov', 'flv', 'wmv'))

configure_uploads(app, (images, videos, multimedia))

@app.route('/post/create', methods=['GET', 'POST'])
def create_media():
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		image = images.save(request.files['image'])
		video = videos.save(request.files['video'])
		multimedia_file = multimedia.save(request.files['multimedia'])
		new_media = Post(title=title, content=content, multimedia=multimedia_file, image=image, video=video) 
		db.session.add(new_media)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('create_post.html')
