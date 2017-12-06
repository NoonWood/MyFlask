from flask import Blueprint
from flask import render_template
from flask_login import current_user
from models import Post, Tag, User

from flask import request
from .forms import PostForm

from app import db
from flask import redirect, url_for

from flask_security import login_required

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods={'POST', 'GET'})
@login_required
def create_post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        #tags = request.form['tags']
        try:
            post = Post(title=title, body=body)
            post.authors.append(current_user)
            #tag = Tag(name=tags)
            #db.session.add(tag)
            #db.session.commit()
            #post.tags.append(tag)
            #add_tags_to_post(post, parse_tags(tags))
            db.session.add(post)
            db.session.commit()
        except:
            print('Something wrong!')

        return redirect(url_for('posts.index'))

    return render_template('posts/create_post.html', form=form)

'''
def parse_tags(tag_string):
    tags_slugs = tag_string.split(' ')
    return [Tag(name=tag) for tag in tags_slugs]

def add_tags_to_post(post, tags):
    for tag in tags:
        post.tags.append(tag)
'''

@posts.route('/')
def index():
    #Поиск
    q = request.args.get('q')
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)) #.all()
        print(posts)
    else:
        posts = Post.query.order_by(Post.timestamp.desc())
        print(posts)

    pages = posts.paginate(page=page, per_page=5)
    return render_template('posts/index.html', posts=posts, pages=pages)


#TODO slug + id - для полной уникальности
@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug==slug).first_or_404()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)

@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first_or_404()
    posts = tag.posts.all()
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)

@posts.route('/author/posts/<id>')
def author_detail(id):
    posts = Post.query.join(User.posts).filter(User.id == id)
    print(posts)
    author = User.query.get(id)
    return render_template('posts/authors_detail.html', posts=posts, author=author)


@posts.route('/<slug>/edit/', methods=['POST','GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug==slug).first_or_404()
    print(post.authrs)
    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('posts.post_detail', slug=post.slug))
    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form)
