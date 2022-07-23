from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Telling the Flask App where the database will be stored
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlbase.db'
db = SQLAlchemy(app)

def DataBaseInit():
    from app import db
    db.create_all()
    return redirect('/')

# Creating Models to structure data in database
class BlogPost(db.Model):
    # affects the database directly
    id = db.Column(db.Integer, primary_key=True) # Creating a primary key identifier for each BlogPost Model Object created.
    title = db.Column(db.String(100), nullable=False, default='N/A')
    content = db.Column(db.Text, nullable=False, default='N/A')
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().date())
    
    # Returning a new blogpost
    def __repr__(self):
        return 'Blog Post ' + str(self.id)
    
class CommentPost(db.Model):
    # affects the database directly
    id = db.Column(db.Integer, primary_key=True) # Creating a primary key identifier for each CommentPost Model Object created.
    comment_title = db.Column(db.String(100), nullable=False, default='')
    comment_content = db.Column(db.Text, nullable=False, default='')
    comment_author = db.Column(db.String(20), nullable=False, default='')
    comment_track = db.Column(db.Integer, nullable=False)
    comment_date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().date())
    
    # Returning a new commentpost
    def __repr__(self):
        return 'Comment Post ' + str(self.id)

# Creates, Initializes and Serves-Up the database
DataBaseInit()

@app.route('/')
def index():
    return render_template('index.html', title='CS CODING-DOJO')

# POSTS CODE SECTION #

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    post_count = len(BlogPost.query.all())
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post) #saves only in runtime
        db.session.commit() #saves forever
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', count=post_count, posts=all_posts, title='Posts')

    
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    post = BlogPost.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post, title='Edit Post')

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html', title='New Post')


# COMMENTS CODE SECTION #
    
@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if len(BlogPost.query.all()) == 0:
        return redirect('/posts')
    else:
        post_length = len(CommentPost.query.all())
        post_count = 0
        for i in range(post_length):
            if CommentPost.query.get(i+1).comment_title != '':
                post_count += 1
            else:
                pass
        
        if request.method == 'POST':
            post_title = request.form['comment_title']
            post_content = request.form['comment_content']
            post_author = request.form['comment_author']
            post_refer = request.form['comment_track']
            new_post = CommentPost(comment_title=post_title, comment_content=post_content, comment_author=post_author, comment_track=post_refer)
            db.session.add(new_post) #saves only in runtime
            db.session.commit() #saves forever
            post_count += 1
            return redirect('/comments')
        else:
            all_comments = CommentPost.query.order_by(CommentPost.comment_date_posted).all()
            return render_template('comments.html', count=post_count, comments=all_comments, title='Post Comments')

    
@app.route('/comments/delete/<int:id>')
def comment_delete(id):
    post = CommentPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/comments')


@app.route('/comments/edit_comment/<int:id>', methods=['GET', 'POST'])
def edit_comment(id):
    
    post = CommentPost.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form['comment_title']
        post.author = request.form['comment_author']
        post.content = request.form['comment_content']
        post.refer = request.form['comment_track']
        db.session.commit()
        return redirect('/comments')
    else:
        return render_template('edit_comment.html', comment_post=post, title='Edit Comment')

@app.route('/comments/new_comment', methods=['GET', 'POST'])
def new_comment():
    if len(BlogPost.query.all()) == 0:
        return redirect('/posts')
    else:
        if request.method == 'POST':
            post.title = request.form['comment_title']
            post.author = request.form['comment_author']
            post.content = request.form['comment_content']
            new_post = CommentPost(comment_title=post_title, comment_content=post_content, comment_author=post_author)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/comments')
        else:
            return render_template('new_comment.html', title='New Comment')
    

# SERVER STARTUP CODE #
if __name__ == '__main__':
    app.run(port=8080, debug=True)