from flask import render_template, redirect, url_for, request
from flask_uploads import UploadSet, configure_uploads
from . import db, create_app
from app.static import Video


app = create_app()

videos = UploadSet('videos', ('mp4', 'avi', 'mov', 'flv', 'wmv'))

configure_uploads(app, videos)


@app.route('/')
def home():
    # Fetch videos from the database
    videos = Video.query.all()
    # Render the 'home.html' template, passing the videos to the template
    return render_template('home.html', videos=videos)


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
	return render_template('create_video.html')
