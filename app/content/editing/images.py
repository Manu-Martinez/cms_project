from flask import render_template, redirect, url_for, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from . import db, create_app
from app.static.models import Post


app = create_app()

images = UploadSet('images', IMAGES)

configure_uploads(app, images)

@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		image = images.save(request.files['image'])
		new_post = Post(title=title, content=content, image=image) 
		db.session.add(new_post)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('create_post.html')
