from flask import render_template, redirect, url_for, request
from . import create_app, db
from .models import User, Post

app = create_app()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = user.posts.all()
	links = user.links.all()
	videos = user.videos.all()
	photos = user.photos.all()
	return render_template('user.html', user=user, posts=posts, links=links, videos=videos, photos=photos)

@app.route('/get-user/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
	post = Post.query.get_or_404(post_id)
	if request.method == 'POST':
		post.content = request.form['content']
		db.session.commit()
		return redirect(url_for('user', username=post.author.username))
	return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('home'))
