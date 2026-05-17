"""种子数据脚本 - 导入模拟数据"""
from app import create_app
from utils import get_db, now
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db = get_db()

    # 清空（按依赖顺序）
    for t in ['post_likes', 'posts', 'articles', 'users']:
        db.execute(f'DELETE FROM {t}')
    # 重置自增计数器
    db.execute("DELETE FROM sqlite_sequence")

    # === 用户 ===
    db.execute(
        '''INSERT INTO users (student_id, username, password, email, phone, gender, height, weight)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        ('2024001', '测试用户', generate_password_hash('123456'),
         'test@example.com', '138****8888', 1, 175.0, 65.0)
    )

    # === 文章（3篇）===
    articles = [
        ('食堂"减脂餐"点菜攻略：如何避开高油雷区？',
         '校内食堂其实隐藏着很多健康组合，本期我们实地走访了第一食堂和第二食堂...',
         '<p>每到饭点，食堂里琳琅满目的菜品让人眼花缭乱。但你知道吗？看起来健康的菜品背后可能隐藏着高热量的陷阱。</p><p>本期我们采访了学校营养学专业的李教授，为大家整理了一份食堂点菜攻略...</p>',
         '饮食指导', 'bg-emerald-100 text-emerald-600',
         'https://modao.cc/agent-py/media/generated_images/2026-03-26/f3b0e445267d4e72a162aefd48896059.jpg',
         'College students eating healthy', 1200),
        ('宿舍党福音：一张瑜伽垫，搞定全身塑形',
         '不需要昂贵的私教课和复杂的健身房设备，在宿舍也能轻松锻炼出马甲线...',
         '<p>对于大部分在校大学生来说，健身房年卡是一笔不小的开销。但其实，只需要一张瑜伽垫，你就能在宿舍完成全身训练。</p><p>我们邀请了体育学院的王教练，为大家设计了一套专属的宿舍训练方案...</p>',
         '运动健身', 'bg-orange-100 text-orange-600',
         'https://modao.cc/agent-py/media/generated_images/2026-03-26/f2eaa8c06367411ebc4f98cae483627e.jpg',
         'Student exercising in dorm', 890),
        ('拒绝容貌焦虑：如何在这场"美丽竞争"中找回自我？',
         '当你开始在社交软件里因为别人的精修图而感到自卑时，你应该看看这篇专栏...',
         '<p>打开小红书、抖音，满屏的完美身材和精致面容让人窒息。根据调查，超过70%的大学生表示曾因社交媒体产生过容貌焦虑。</p><p>我们采访了学校心理咨询中心的张老师，她从专业角度分析了容貌焦虑的成因...</p>',
         '心理调适', 'bg-blue-100 text-blue-600',
         'https://modao.cc/agent-py/media/generated_images/2026-03-26/ca1285ba30014ddd88fa56b0d7135e9e.jpg',
         'Stress relief meditation', 2500),
    ]
    for a in articles:
        db.execute(
            '''INSERT INTO articles
               (title, excerpt, content, tag, tag_class, img_url, img_alt, views, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (*a, now(), now())
        )

    # === 匿名帖子（3条，固定时间以模拟真实发帖顺序）===
    posts_data = [
        (1, '校友 #12938', '图书馆闭馆时的星光真的好美，虽然考研的路很难，但我觉得我还能坚持。大家加油呀！✨', 42, 5, '2025-08-15 14:23:56'),
        (1, '校友 #12901', '今天的午饭好咸，第一食堂那个大叔是不是手抖了...[大哭]', 12, 3, '2026-03-07 09:45:12'),
        (1, '校友 #12885', '拒绝了不想去的社团聚餐，瞬间感觉整个人都自由了，社恐人的胜利！', 88, 16, '2024-11-22 20:08:39'),
    ]
    for p in posts_data:
        db.execute(
            '''INSERT INTO posts (user_id, author, content, likes, comments, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (*p[:5], p[5], p[5])
        )

    db.commit()
    print('[OK] 种子数据导入成功!')
    print('  - 1 个测试用户 (学号: 2024001, 密码: 123456)')
    print('  - 3 篇健康文章')
    print('  - 3 条匿名树洞帖子')
