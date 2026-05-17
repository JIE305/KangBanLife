from flask import jsonify
import sqlite3
from config import Config
from datetime import datetime, date


def get_db():
    db = sqlite3.connect(Config.DATABASE, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def success(data=None, message='操作成功', code=200):
    resp = {'code': code, 'message': message}
    if data is not None:
        resp['data'] = data
    return jsonify(resp), code


def error(message='请求失败', code=400, errors=None):
    resp = {'code': code, 'message': message}
    if errors:
        resp['errors'] = errors
    return jsonify(resp), code


def paginated_response(items, total, page, limit):
    return success({
        'items': items,
        'total': total,
        'page': page,
        'limit': limit
    })


def row_to_dict(row):
    return dict(row) if row else None


def rows_to_list(rows):
    return [dict(r) for r in rows]


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
