import os
import uuid

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from config import Config
from utils import get_db, success, error, row_to_dict, now

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE id = ?', (get_jwt_identity(),)
    ).fetchone()
    if not user:
        return error('用户不存在', 404)

    user_dict = row_to_dict(user)
    user_dict.pop('password')
    return success({'user': user_dict})


@user_bp.route('/profile/basic', methods=['PUT'])
@jwt_required()
def update_basic():
    user_id = get_jwt_identity()
    data = request.get_json()

    allowed = ['username', 'gender', 'height', 'weight']
    fields = {k: data[k] for k in allowed if k in data}

    if not fields:
        return error('没有需要更新的字段', 400)
    if 'gender' in fields and fields['gender'] not in (0, 1, 2):
        return error('性别值无效', 400)

    db = get_db()
    set_clause = ', '.join(f'{k} = ?' for k in fields)
    values = list(fields.values()) + [now(), user_id]
    db.execute(f'UPDATE users SET {set_clause}, updated_at = ? WHERE id = ?', values)
    db.commit()

    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    user_dict = row_to_dict(user)
    user_dict.pop('password')
    return success({'user': user_dict}, '基本信息已更新')


@user_bp.route('/profile/contact', methods=['PUT'])
@jwt_required()
def update_contact():
    user_id = get_jwt_identity()
    data = request.get_json()

    fields = {}
    if 'email' in data:
        fields['email'] = data['email']
    if 'phone' in data:
        phone = data['phone']
        if len(phone) >= 11:
            phone = phone[:3] + '****' + phone[7:]
        fields['phone'] = phone

    if not fields:
        return error('没有需要更新的字段', 400)

    db = get_db()
    set_clause = ', '.join(f'{k} = ?' for k in fields)
    values = list(fields.values()) + [now(), user_id]
    db.execute(f'UPDATE users SET {set_clause}, updated_at = ? WHERE id = ?', values)
    db.commit()
    return success(message='联系方式已更新')


@user_bp.route('/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    user_id = get_jwt_identity()

    if 'file' not in request.files:
        return error('请选择文件', 400)

    file = request.files['file']
    if not file.filename:
        return error('请选择文件', 400)

    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in Config.ALLOWED_EXTENSIONS:
        return error('仅支持 jpg/png/gif/webp 格式', 400)

    # 检查文件大小
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > Config.MAX_CONTENT_LENGTH:
        return error('图片大小不能超过5MB', 413)

    filename = secure_filename(f'{user_id}_{uuid.uuid4().hex[:8]}.{ext}')
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)

    avatar_url = f'/uploads/{filename}'
    db = get_db()
    db.execute(
        'UPDATE users SET avatar_url = ?, updated_at = ? WHERE id = ?',
        (avatar_url, now(), user_id)
    )
    db.commit()
    return success({'avatar_url': avatar_url}, '头像上传成功')
