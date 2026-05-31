from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from utils import get_db
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    CORS(app, origins='*', supports_credentials=True)

    JWTManager(app)

    # 初始化数据库
    _init_schema_if_needed(app)

    # 静态文件服务 - 头像
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # 注册蓝图
    from auth import auth_bp
    from api.user import user_bp
    from api.articles import articles_bp
    from api.posts import posts_bp
    from api.resources import resources_bp
    from api.chat import chat_bp
    from api.matches import matches_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(user_bp, url_prefix='/api/v1/user')
    app.register_blueprint(articles_bp, url_prefix='/api/v1/articles')
    app.register_blueprint(posts_bp, url_prefix='/api/v1/posts')
    app.register_blueprint(resources_bp, url_prefix='/api/v1/resources')
    app.register_blueprint(chat_bp, url_prefix='/api/v1/chat')
    app.register_blueprint(matches_bp, url_prefix='/api/v1/matches')

    return app


def _init_schema_if_needed(app):
    """首次运行时自动创建数据库表"""
    import os
    schema_file = os.path.join(app.config['BASE_DIR'], 'schema_lite.sql')
    if not os.path.exists(schema_file):
        return

    db = get_db()
    cursor = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if cursor.fetchone() is None:
        with open(schema_file, 'r', encoding='utf-8') as f:
            db.executescript(f.read())
        db.commit()
    db.close()


if __name__ == '__main__':
    app = create_app()
    print('UniHealth API Server: http://localhost:5000')
    app.run(debug=True, port=5000)
