from flask import Blueprint, request
from utils import get_db, success, error, rows_to_list, row_to_dict, paginated_response

articles_bp = Blueprint('articles', __name__)


@articles_bp.route('', methods=['GET'])
def get_articles():
    tag = request.args.get('tag')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    page = max(1, page)
    limit = min(50, max(1, limit))

    db = get_db()
    where = "WHERE status = 1"
    params = []
    if tag:
        where += " AND tag = ?"
        params.append(tag)

    total = db.execute(
        f'SELECT COUNT(*) FROM articles {where}', params
    ).fetchone()[0]

    rows = db.execute(
        f'''SELECT id, title, excerpt, tag, tag_class, img_url, img_alt, views, created_at
            FROM articles {where}
            ORDER BY created_at DESC LIMIT ? OFFSET ?''',
        params + [limit, (page - 1) * limit]
    ).fetchall()

    items = []
    for r in rows:
        d = dict(r)
        d['date'] = d.pop('created_at', '')[:10]
        d['tagClass'] = d.pop('tag_class', '')
        d['img'] = d.pop('img_url', '')
        d['alt'] = d.pop('img_alt', '')
        items.append(d)

    return paginated_response(items, total, page, limit)


@articles_bp.route('/featured', methods=['GET'])
def get_featured():
    limit = request.args.get('limit', 3, type=int)
    limit = min(10, max(1, limit))

    rows = get_db().execute(
        '''SELECT id, title, excerpt, tag, tag_class, img_url, img_alt, views, created_at
           FROM articles WHERE status = 1 ORDER BY views DESC LIMIT ?''',
        (limit,)
    ).fetchall()

    items = []
    for r in rows:
        d = dict(r)
        d['date'] = d.pop('created_at', '')[:10]
        d['tagClass'] = d.pop('tag_class', '')
        d['img'] = d.pop('img_url', '')
        d['alt'] = d.pop('img_alt', '')
        items.append(d)

    return success({'items': items})


@articles_bp.route('/<int:id>', methods=['GET'])
def get_article(id):
    db = get_db()
    article = db.execute(
        'SELECT * FROM articles WHERE id = ? AND status = 1', (id,)
    ).fetchone()
    if not article:
        return error('文章不存在', 404)

    db.execute('UPDATE articles SET views = views + 1 WHERE id = ?', (id,))
    db.commit()

    d = row_to_dict(article)
    d['date'] = d.pop('created_at', '')[:10]
    d['tagClass'] = d.pop('tag_class', '')
    d['img'] = d.pop('img_url', '')
    d['alt'] = d.pop('img_alt', '')
    return success({'article': d})
