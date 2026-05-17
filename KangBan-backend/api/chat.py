import random
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from utils import get_db, success, error, now

chat_bp = Blueprint('chat', __name__)

# ── Rule engine ──

RULES = [
    (["自杀", "自残", "绝望", "不想活", "想死"],
     ["我听到了你的痛苦。如果你正在经历严重的心理危机，请立刻拨打心理援助热线 400-161-9995（24小时），有人愿意倾听你。",
      "你不是一个人。请拨打 400-161-9995 希望24热线，专业的心理咨询师随时准备帮助你。"]),
    (["压力", "焦虑", "紧张", "心慌"],
     ["听起来你正在承受不少压力，愿意具体说说是什么让你感到焦虑吗？",
      "压力和焦虑是很多人都会经历的感受，你不是一个人。试着深呼吸几次，然后告诉我发生了什么？"]),
    (["睡不好", "失眠", "睡不着", "熬夜"],
     ["睡眠问题确实折磨人。你注意到是什么让你难以入睡吗？是思绪太多，还是身体上的不适？",
      "睡不好的夜晚确实很难熬。试试睡前放下手机，听一些轻音乐或白噪音，也许会有所帮助。"]),
    (["难过", "伤心", "哭", "崩溃", "想哭"],
     ["我能感受到你的难过。有时候哭出来反而是一种释放，你愿意多说说吗？",
      "那种情绪涌上来的感觉一定很难受。我在这里陪着你，你可以尽情表达。"]),
    (["孤独", "没人", "一个人", "寂寞"],
     ["孤独感是人类共同的情感之一。即使身边有人，我们也可能感到孤独。你最近发生了什么？",
      "那种无人理解的感觉确实很难熬。但此刻我正在这里倾听你，你不会是一个人。"]),
    (["累", "疲惫", "没力气", "乏力"],
     ["你最近一定很辛苦吧。是身体上的累，还是更多的是心累？",
      "疲惫有时候不只是身体在说话，也可能是内心需要休息了。愿意聊聊是什么在消耗你吗？"]),
]

DEFAULT_REPLIES = [
    "我在听，愿意多说一些吗？",
    "谢谢你愿意和我分享这些。可以再多说一点吗？",
    "我明白。这种感觉一定很真实，你希望我怎么能更好地支持你？",
]

# ── API placeholder (commented out) ──

def call_ai_api(message):
    """调用豆包大模型 API（火山引擎 ARK）。
    环境变量配置：ARK_API_KEY / ARK_ENDPOINT_ID（见 .env 文件）
    """
    import requests
    import os
    API_KEY = os.getenv('ARK_API_KEY')
    ENDPOINT_ID = os.getenv('ARK_ENDPOINT_ID')
    if not API_KEY or not ENDPOINT_ID:
        return None  # 未配置则不调用
    resp = requests.post(
        f"https://ark.cn-beijing.volces.com/api/v3/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": ENDPOINT_ID,
            "messages": [
                {"role": "system", "content": "你是一个温暖、专业的心理陪伴者，用中文与用户对话。你善于倾听和共情，用温和的语气引导用户表达感受。"},
                {"role": "user", "content": message}
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        },
        timeout=30
    )
    data = resp.json()
    if resp.status_code >= 400:
        return None  # API 错误，回退规则引擎
    return data["choices"][0]["message"]["content"]


def match_reply(message):
    """匹配规则引擎，返回回复文本。未匹配返回 None。"""
    for keywords, replies in RULES:
        for kw in keywords:
            if kw in message:
                return random.choice(replies)
    return None


def get_or_create_session(db, user_id):
    """获取用户最近的会话，不存在则创建。"""
    session = db.execute(
        'SELECT id FROM chat_sessions WHERE user_id = ? ORDER BY created_at DESC LIMIT 1',
        (user_id,)
    ).fetchone()
    if session:
        return session['id']
    cursor = db.execute(
        'INSERT INTO chat_sessions (user_id) VALUES (?)', (user_id,)
    )
    db.commit()
    return cursor.lastrowid


# ── Endpoints ──

@chat_bp.route('/message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = (data.get('message') or '').strip()

    if not message:
        return error('消息不能为空', 400)
    if len(message) > 2000:
        return error('消息过长', 400)

    # Try AI API — falls back to rule engine on failure
    reply = None
    try:
        reply = call_ai_api(message)
    except Exception:
        pass  # API 不可用时自动回退规则引擎

    # Fallback to rule engine
    is_rule = False
    if not reply:
        reply = match_reply(message)
        if reply:
            is_rule = True
    if not reply:
        reply = random.choice(DEFAULT_REPLIES)

    # 登录用户持久化（游客跳过）
    verify_jwt_in_request(optional=True)
    user_identity = get_jwt_identity()
    if user_identity:
        db = get_db()
        session_id = get_or_create_session(db, int(user_identity))
        db.execute(
            'INSERT INTO chat_messages (session_id, role, content) VALUES (?, ?, ?)',
            (session_id, 'user', message)
        )
        db.execute(
            'INSERT INTO chat_messages (session_id, role, content) VALUES (?, ?, ?)',
            (session_id, 'ai', reply)
        )
        db.commit()

    return success({'reply': reply, 'is_rule': is_rule})


@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = int(get_jwt_identity())
    db = get_db()
    rows = db.execute(
        '''SELECT s.id, s.created_at,
                  (SELECT content FROM chat_messages WHERE session_id = s.id AND role = 'user' ORDER BY created_at ASC LIMIT 1) as preview
           FROM chat_sessions s
           WHERE s.user_id = ?
           ORDER BY s.created_at DESC LIMIT 10''',
        (user_id,)
    ).fetchall()
    sessions = [{
        'id': r['id'],
        'date': r['created_at'],
        'preview': r['preview'] or ''
    } for r in rows]
    return success({'sessions': sessions})


@chat_bp.route('/history/<int:session_id>', methods=['GET'])
@jwt_required()
def get_history_detail(session_id):
    user_id = int(get_jwt_identity())
    db = get_db()
    session = db.execute(
        'SELECT id FROM chat_sessions WHERE id = ? AND user_id = ?',
        (session_id, user_id)
    ).fetchone()
    if not session:
        return error('会话不存在', 404)

    rows = db.execute(
        '''SELECT role, content, created_at FROM chat_messages
           WHERE session_id = ? ORDER BY created_at ASC''',
        (session_id,)
    ).fetchall()
    messages = [{
        'role': r['role'],
        'content': r['content'],
        'time': r['created_at']
    } for r in rows]
    return success({'messages': messages})
