from flask import render_template, redirect, url_for, request
from . import db, create_app
from app.static import Post


app = create_app()

@app.route('/')
def home():
    # Fetch posts from the database
    posts = Post.query.all()
    # Render the 'home.html' template, passing the posts to the template
    return render_template('home.html', posts=posts)

@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html')