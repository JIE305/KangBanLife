from flask import Blueprint, request
from utils import get_db, success, error, rows_to_list

resources_bp = Blueprint('resources', __name__)


@resources_bp.route('/first-aid', methods=['GET'])
def get_first_aid():
    rows = get_db().execute(
        'SELECT title, description, icon, bg_class, border_class, icon_class,'
        ' icon_hover_class, title_class, desc_class'
        ' FROM first_aid_resources WHERE status = 1 ORDER BY sort_order'
    ).fetchall()

    items = []
    for r in rows:
        items.append({
            'title': r['title'],
            'desc': r['description'],
            'icon': r['icon'],
            'bgClass': r['bg_class'],
            'borderClass': r['border_class'],
            'iconClass': r['icon_class'],
            'iconHoverClass': r['icon_hover_class'],
            'titleClass': r['title_class'],
            'descClass': r['desc_class']
        })
    return success({'items': items})


@resources_bp.route('/medicines', methods=['GET'])
def get_medicines():
    rows = get_db().execute(
        'SELECT title, description, icon, icon_bg, icon_color, tag, tag_class'
        ' FROM medicines WHERE status = 1 ORDER BY sort_order'
    ).fetchall()

    items = []
    for i, r in enumerate(rows):
        border = '' if i == 0 else 'border-t border-slate-50'
        items.append({
            'title': r['title'],
            'desc': r['description'],
            'icon': r['icon'],
            'iconBg': r['icon_bg'],
            'iconColor': r['icon_color'],
            'tag': r['tag'],
            'tagClass': r['tag_class'],
            'borderClass': border
        })
    return success({'items': items})


@resources_bp.route('/facilities', methods=['GET'])
def get_facilities():
    keyword = request.args.get('keyword', '').strip()
    ftype = request.args.get('type', '').strip()

    db = get_db()
    where = 'WHERE status = 1'
    params = []

    if keyword:
        where += ' AND (name LIKE ? OR address LIKE ?)'
        params.extend([f'%{keyword}%', f'%{keyword}%'])
    if ftype:
        where += ' AND type LIKE ?'
        params.append(f'%{ftype}%')

    rows = db.execute(
        f'SELECT id, name, address, lat, lng, distance, walk_time, rating, type, tag, tag_class, tel'
        f' FROM medical_facilities {where} ORDER BY distance'
    ).fetchall()

    items = []
    for r in rows:
        items.append({
            'id': r['id'],
            'name': r['name'],
            'address': r['address'],
            'lat': r['lat'],
            'lng': r['lng'],
            'distance': r['distance'],
            'walkTime': r['walk_time'],
            'rating': r['rating'],
            'type': r['type'],
            'tag': r['tag'],
            'tagClass': r['tag_class'],
            'tel': r['tel']
        })
    return success({'items': items})


@resources_bp.route('/search', methods=['GET'])
def search_resources():
    q = request.args.get('q', '').strip()
    if not q:
        return error('请输入搜索关键词', 400)

    db = get_db()
    like = f'%{q}%'

    first_aid = rows_to_list(db.execute(
        'SELECT title, description FROM first_aid_resources WHERE status = 1 AND (title LIKE ? OR description LIKE ?)',
        (like, like)
    ).fetchall())
    medicines = rows_to_list(db.execute(
        'SELECT title, description FROM medicines WHERE status = 1 AND (title LIKE ? OR description LIKE ?)',
        (like, like)
    ).fetchall())
    facilities = rows_to_list(db.execute(
        'SELECT name, address, distance, type FROM medical_facilities WHERE status = 1 AND (name LIKE ? OR address LIKE ? OR type LIKE ?)',
        (like, like, like)
    ).fetchall())

    return success({
        'results': {
            'first_aid': first_aid,
            'medicines': medicines,
            'facilities': facilities
        }
    })
