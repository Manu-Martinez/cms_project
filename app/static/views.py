from flask import render_template, redirect, url_for, request
from app import db
from .models import User, Post
from flask import current_app as app
from flask_login import current_user

@app.route('/')
def home():
	return render_template('home.html')


@app.route('/create-user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        # Add more fields as necessary

        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('user', username=username))

    return render_template('create_user.html')

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



@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		# Assuming the user is logged in and you have access to current_user
		user_id = current_user.id

		post = Post(title=title, content=content, user_id=user_id)
		db.session.add(post)
		db.session.commit()

		return redirect(url_for('get_post', post_id=post.id))

	return render_template('create_post.html')

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
