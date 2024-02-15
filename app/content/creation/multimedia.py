from flask import render_template, redirect, url_for, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, AUDIO, DATA
from . import db, create_app
from app.static.models import Post, Link, Video, Photo
from . import images, videos

app = create_app()

multimedia = UploadSet('multimedia', AUDIO + DATA)
images = UploadSet('images', IMAGES)
videos = UploadSet('videos', ('mp4', 'avi', 'mov', 'flv', 'wmv'))

configure_uploads(app, (images, videos, multimedia))

@app.route('/')
def home():
    # Fetch media from the database
    posts = Post.query.all()
    links = Link.query.all()
    photos = Photo.query.all()
    videos = Video.query.all()

    # Combine all media into a single list
    media = posts + links + photos + videos

    # Render the 'home.html' template, passing the media to the template
    return render_template('home.html', media=media)

@app.route('/post/create', methods=['GET', 'POST'])
def create_media():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_file = request.files.get('image')
        video_file = request.files.get('video')
        multimedia_file = request.files.get('multimedia')

        image = images.save(image_file) if image_file else None
        video = videos.save(video_file) if video_file else None
        multimedia = multimedia.save(multimedia_file) if multimedia_file else None

        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()  # commit new_post first to get its id

        if image:
            new_photo = Photo(post_id=new_post.id, image=image)
            db.session.add(new_photo)

        if video:
            new_video = Video(post_id=new_post.id, video=video)
            db.session.add(new_video)

        if multimedia:
            new_link = Link(post_id=new_post.id, multimedia=multimedia)
            db.session.add(new_link)

        db.session.commit()  # commit the rest
        return redirect(url_for('home'))

    return render_template('create_media.html')