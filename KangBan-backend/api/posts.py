import random

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils import get_db, success, error, row_to_dict, paginated_response, now

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    page = max(1, page)
    limit = min(50, max(1, limit))

    db = get_db()
    total = db.execute(
        'SELECT COUNT(*) FROM posts WHERE status = 1'
    ).fetchone()[0]

    rows = db.execute(
        '''SELECT id, author, content, likes, comments, created_at
           FROM posts WHERE status = 1
           ORDER BY created_at DESC LIMIT ? OFFSET ?''',
        (limit, (page - 1) * limit)
    ).fetchall()

    items = [{
        'id': r['id'],
        'author': r['author'],
        'content': r['content'],
        'likes': r['likes'],
        'comments': r['comments'],
        'time': r['created_at']
    } for r in rows]

    return paginated_response(items, total, page, limit)


@posts_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    content = (data.get('content') or '').strip()

    if not content:
        return error('内容不能为空', 400)
    if len(content) > 1000:
        return error('内容不能超过1000字', 400)

    author = f"校友 #{random.randint(10000, 99999)}"
    db = get_db()
    cursor = db.execute(
        'INSERT INTO posts (user_id, author, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?)',
        (user_id, author, content, now(), now())
    )
    db.commit()

    post = row_to_dict(db.execute(
        'SELECT id, author, content, likes, comments, created_at FROM posts WHERE id = ?',
        (cursor.lastrowid,)
    ).fetchone())
    post['time'] = post.pop('created_at')
    return success({'post': post}, '发布成功', 201)


@posts_bp.route('/<int:id>/like', methods=['POST'])
@jwt_required()
def toggle_like(id):
    user_id = int(get_jwt_identity())
    db = get_db()

    # 检查帖子是否存在
    post = db.execute(
        'SELECT id FROM posts WHERE id = ? AND status = 1', (id,)
    ).fetchone()
    if not post:
        return error('帖子不存在', 404)

    existing = db.execute(
        'SELECT id FROM post_likes WHERE post_id = ? AND user_id = ?',
        (id, user_id)
    ).fetchone()

    if existing:
        # 取消点赞
        db.execute('DELETE FROM post_likes WHERE id = ?', (existing['id'],))
        db.execute('UPDATE posts SET likes = MAX(0, likes - 1) WHERE id = ?', (id,))
        db.commit()
        likes = db.execute(
            'SELECT likes FROM posts WHERE id = ?', (id,)
        ).fetchone()['likes']
        return success({'likes': likes, 'is_liked': False})
    else:
        # 点赞
        db.execute(
            'INSERT INTO post_likes (post_id, user_id) VALUES (?, ?)', (id, user_id)
        )
        db.execute('UPDATE posts SET likes = likes + 1 WHERE id = ?', (id,))
        db.commit()
        likes = db.execute(
            'SELECT likes FROM posts WHERE id = ?', (id,)
        ).fetchone()['likes']
        return success({'likes': likes, 'is_liked': True})


@posts_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    user_id = int(get_jwt_identity())
    db = get_db()
    post = db.execute(
        'SELECT user_id FROM posts WHERE id = ? AND status = 1', (id,)
    ).fetchone()
    if not post:
        return error('帖子不存在', 404)
    if post['user_id'] != user_id:
        return error('无权删除他人的帖子', 403)

    db.execute('UPDATE posts SET status = 0 WHERE id = ?', (id,))
    db.commit()
    return success(message='帖子已删除')
