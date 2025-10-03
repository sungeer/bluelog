from flask import g, abort

from bluelog.models.model_post import PostModel


def get_post_by_id(post_id, check_author=True):
    post = PostModel().get_post_by_id(post_id)
    if post is None:
        abort(404, f'Post id {id} does not exist.')
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post
