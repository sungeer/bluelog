from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

from bluelog.decorators import login_required
from bluelog.services import service_post
from bluelog.models.model_post import PostModel
from bluelog.utils import util_time

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    posts = ''
    return render_template('blog/index.html', posts=posts)


@blog_bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            author_id = g.user['id']
            created_at = util_time.get_now()
            PostModel().add_post(title, body, author_id, created_at)
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


@blog_bp.route('/<int:post_id>/update', methods=('GET', 'POST'))
@login_required
def update(post_id):
    post = service_post.get_post_by_id(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            PostModel().update_post(title, body, post_id)
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@blog_bp.route('/<int:post_id>/delete', methods=('POST',))
@login_required
def delete(post_id):
    service_post.get_post_by_id(post_id)
    PostModel().delete_post(post_id)
    return redirect(url_for('blog.index'))
