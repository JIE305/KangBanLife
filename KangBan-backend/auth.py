from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from utils import get_db, success, error, row_to_dict, now

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    student_id = data.get('studentId', '').strip()
    password = data.get('password', '').strip()

    if not student_id or not password:
        return error('请填写完整信息', 400)

    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE student_id = ?', (student_id,)
    ).fetchone()

    if not user or not check_password_hash(user['password'], password):
        return error('学号或密码错误', 401)

    user_dict = row_to_dict(user)
    user_dict.pop('password')
    token = create_access_token(identity=str(user['id']))

    return success({'user': user_dict, 'token': token}, '登录成功')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    student_id = data.get('studentId', '').strip()
    username = data.get('username', '').strip()
    phone = data.get('phone', '').strip()
    password = data.get('password', '').strip()

    if not all([student_id, username, phone, password]):
        return error('请填写完整信息', 400)

    if len(password) < 6:
        return error('密码长度不能少于6位', 400)

    db = get_db()
    existing = db.execute(
        'SELECT id FROM users WHERE student_id = ? OR username = ?',
        (student_id, username)
    ).fetchone()
    if existing:
        return error('该学号或用户名已被注册', 409)

    hashed = generate_password_hash(password)
    masked_phone = phone[:3] + '****' + phone[7:] if len(phone) >= 11 else phone

    cursor = db.execute(
        '''INSERT INTO users (student_id, username, password, phone, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (student_id, username, hashed, masked_phone, now(), now())
    )
    db.commit()

    user = db.execute(
        'SELECT * FROM users WHERE id = ?', (cursor.lastrowid,)
    ).fetchone()
    user_dict = row_to_dict(user)
    user_dict.pop('password')
    token = create_access_token(identity=str(user['id']))

    return success({'user': user_dict, 'token': token}, '注册成功', 201)


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return success(message='登出成功')
