from flask import render_template, request
from flask_login import login_required
from app.static.models import Post
from app import main, app
from flask import jsonify
from app.versionControl.revisions import Revision

@main.route('/')
def home():
	# Get the page number from the query parameters (default to 1 if not provided)
	page = request.args.get('page', 1, type=int)

	# Fetch the published posts from the database, ordered by publication date,
	# and paginate them (10 per page)
	posts = Post.query.filter_by(status='published').order_by(Post.publication_date.desc()).paginate(page, 10, False)

	# Pass the posts to the template
	return render_template('home.html', posts=posts)

@app.route('/create_img')
def create_img():
	return render_template('create_img.html')

@app.route('/create_media')
def create_media():
	return render_template('create_media.html')

@app.route('/create_post')
def create_post():
	return render_template('create_post.html')

@app.route('/create_video')
def create_video():
	return render_template('create_video.html')

@app.route('/edit_post/<int:post_id>')
def edit_post(post_id):
	# Fetch the post using the post_id...
	return render_template('edit_post.html', post=post)

@app.route('/edit_user/<int:user_id>')
def edit_user(user_id):
	# Fetch the user using the user_id...
	return render_template('edit_user.html', user=user)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	return render_template('logout.html')

@app.route('/post/<int:post_id>')
def post(post_id):
	# Fetch the post using the post_id...
	return render_template('post.html', post=post)

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/upload')
def upload():
	return render_template('upload.html')

@app.route('/user/<int:user_id>')
def user(user_id):
    # Fetch the user using the user_id...
    return render_template('user.html', user=user)


@post.route('/post_revisions/<int:id>', methods=['GET'])
@login_required
def post_revisions(id):
    # Fetch all revisions for the post
    revisions = Revision.query.filter_by(post_id=id).order_by(Revision.created_at.desc()).all()

    # Convert the revisions to a JSON-serializable format
    revisions_json = [{'id': rev.id, 'content': rev.content, 'image_path': rev.image_path, 'video_url': rev.video_url, 'link_url': rev.link_url, 'created_at': rev.created_at} for rev in revisions]

    return jsonify(revisions_json)