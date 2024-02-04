from flask import render_template, redirect, url_for, request
from flask_uploads import UploadSet, configure_uploads, AUDIO, DATA
from . import db, create_app
from app.static import Video
from flask_uploads import videos


app = create_app()

videos = UploadSet('videos', ('mp4', 'avi', 'mov', 'flv', 'wmv'))

configure_uploads(app, videos)

@app.route('/post/create', methods=['GET', 'POST'])
def create_video():
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		video = videos.save(request.files['video'])
		new_video = Video(title=title, content=content, video=video) 
		db.session.add(new_video)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('create_post.html')
