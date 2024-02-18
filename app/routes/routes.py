from flask import render_template, request
from app.static.models import Post
from app import main
@main.route('/')
def home():
	# Get the page number from the query parameters (default to 1 if not provided)
	page = request.args.get('page', 1, type=int)

	# Fetch the published posts from the database, ordered by publication date,
	# and paginate them (10 per page)
	posts = Post.query.filter_by(status='published').order_by(Post.publication_date.desc()).paginate(page, 10, False)

	# Pass the posts to the template
	return render_template('home.html', posts=posts)
