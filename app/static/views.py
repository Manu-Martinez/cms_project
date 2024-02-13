from flask import render_template, flash, abort, redirect, url_for, request
from app import db
from .models import User, Post
from .form import RegistrationForm
from flask import current_app as app
from flask_login import current_user, logout_user, login_user, login_required
from flask import abort


# HOME ROUTE #
@app.route('/')
def home():
	return render_template('home.html')

# REGISTER #
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# LOGIN AND LOGOUT #
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None or not user.check_password(request.form['password']):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


#GET USER #
@app.route('/user')
def no_user():
    return render_template('empty_user.html')

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

# EDIT USER PROFILE #
@app.route('/user/<username>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        abort(403)  # Forbidden access
    if request.method == 'POST':
        new_username = request.form['username']
        if User.query.filter_by(username=new_username).first() is not None:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('edit_user', username=user.username))
        user.username = new_username
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=user.username))
    return render_template('edit_user.html', user=user)


# DELETE USER #
@app.route('/user/<username>/delete', methods=['POST'])
@login_required
def delete_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        abort(403)  # Forbidden access
    logout_user()
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted.')
    return redirect(url_for('home'))


#POST ROUTE#
@app.route('/post')
def no_post():
    return render_template('empty_post.html')

# CREATE A POST #
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

# GET A POST #
@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


# EDIT A POST  #
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
	post = Post.query.get_or_404(post_id)
	if request.method == 'POST':
		post.content = request.form['content']
		db.session.commit()
		return redirect(url_for('user', username=post.author.username))
	return render_template('edit_post.html', post=post)


# DELETE A POST #
@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('home'))
