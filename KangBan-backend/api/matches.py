from flask import Blueprint, request
from utils import get_db, success, error, rows_to_list, paginated_response, now

matches_bp = Blueprint('matches', __name__)

MATCH_SPORTS = ['羽毛球', '篮球', '足球', '乒乓球', '网球', '跑步', '骑行', '游泳', '排球', '其他']
MATCH_TAG_CLASSES = {
    '羽毛球': 'bg-orange-100 text-orange-600',
    '篮球': 'bg-blue-100 text-blue-600',
    '足球': 'bg-emerald-100 text-emerald-600',
    '乒乓球': 'bg-red-100 text-red-600',
    '网球': 'bg-green-100 text-green-600',
    '跑步': 'bg-cyan-100 text-cyan-600',
    '骑行': 'bg-purple-100 text-purple-600',
    '游泳': 'bg-amber-100 text-amber-600',
    '排球': 'bg-indigo-100 text-indigo-600',
    '其他': 'bg-slate-100 text-slate-600',
}


def _ensure_table():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS sport_matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        sport_type VARCHAR(50) NOT NULL,
        tag_class VARCHAR(100),
        time_slot VARCHAR(50),
        location VARCHAR(100),
        description VARCHAR(500),
        creator_name VARCHAR(50),
        status TINYINT DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    db.execute('CREATE INDEX IF NOT EXISTS idx_matches_created_at ON sport_matches(created_at DESC)')
    db.commit()
    db.close()


_ensure_table()


@matches_bp.route('', methods=['GET'])
def get_matches():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    page = max(1, page)
    limit = min(50, max(1, limit))

    db = get_db()
    total = db.execute(
        'SELECT COUNT(*) FROM sport_matches WHERE status = 1'
    ).fetchone()[0]

    rows = db.execute(
        '''SELECT id, sport_type, tag_class, time_slot, location,
                  description, creator_name, created_at
           FROM sport_matches WHERE status = 1
           ORDER BY created_at DESC LIMIT ? OFFSET ?''',
        (limit, (page - 1) * limit)
    ).fetchall()

    items = []
    for r in rows:
        d = dict(r)
        d['sport'] = d.pop('sport_type', '')
        d['tagClass'] = d.pop('tag_class', '')
        d['time'] = d.pop('time_slot', '')
        d['desc'] = d.pop('description', '')
        d['creator'] = d.pop('creator_name', '')
        items.append(d)

    return paginated_response(items, total, page, limit)


@matches_bp.route('', methods=['POST'])
def create_match():
    data = request.get_json(silent=True) or {}

    sport_type = (data.get('sport_type') or data.get('sport') or '').strip()
    if not sport_type:
        return error('请选择运动类型', 400)
    if sport_type not in MATCH_SPORTS:
        return error(f'不支持的运动类型: {sport_type}', 400)

    time_slot = (data.get('time_slot') or data.get('time') or '').strip()
    if not time_slot:
        return error('请填写约球时间', 400)

    location = (data.get('location') or '').strip()
    if not location:
        return error('请填写约球地点', 400)

    description = (data.get('description') or data.get('desc') or '').strip()
    if not description:
        return error('请填写约球描述', 400)
    if len(description) > 500:
        return error('描述不能超过500字', 400)

    creator_name = (data.get('creator_name') or data.get('creator') or '匿名球友').strip()

    tag_class = MATCH_TAG_CLASSES.get(sport_type, 'bg-slate-100 text-slate-600')

    user_id = 1
    try:
        from flask_jwt_extended import get_jwt_identity
        identity = get_jwt_identity()
        if identity:
            user_id = int(identity)
    except Exception:
        pass

    db = get_db()
    cursor = db.execute(
        '''INSERT INTO sport_matches
           (user_id, sport_type, tag_class, time_slot, location, description, creator_name)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (user_id, sport_type, tag_class, time_slot, location, description, creator_name)
    )
    db.commit()

    match_id = cursor.lastrowid
    row = db.execute(
        'SELECT id, sport_type, tag_class, time_slot, location, description, creator_name, created_at FROM sport_matches WHERE id = ?',
        (match_id,)
    ).fetchone()

    d = dict(row)
    d['sport'] = d.pop('sport_type', '')
    d['tagClass'] = d.pop('tag_class', '')
    d['time'] = d.pop('time_slot', '')
    d['desc'] = d.pop('description', '')
    d['creator'] = d.pop('creator_name', '')

    return success({'match': d}, '约球信息发布成功！', 201)


@matches_bp.route('/<int:match_id>', methods=['DELETE'])
def delete_match(match_id):
    db = get_db()
    row = db.execute(
        'SELECT id FROM sport_matches WHERE id = ? AND status = 1', (match_id,)
    ).fetchone()
    if not row:
        return error('约球信息不存在', 404)

    db.execute(
        'UPDATE sport_matches SET status = 0 WHERE id = ?', (match_id,)
    )
    db.commit()
    return success(message='约球信息已删除')