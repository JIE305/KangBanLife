-- ============================================
-- 康伴生活 UniHealth 数据库建表脚本
-- 适用于 SQLite
-- ============================================

-- 1. 用户表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id VARCHAR(20) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    avatar_url VARCHAR(255),
    gender TINYINT DEFAULT 0,
    height DECIMAL(5,2),
    weight DECIMAL(5,2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 健康文章表
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    excerpt VARCHAR(500),
    content TEXT NOT NULL,
    tag VARCHAR(50) DEFAULT '综合',
    tag_class VARCHAR(100),
    img_url VARCHAR(255),
    img_alt VARCHAR(100),
    views INTEGER DEFAULT 0,
    status TINYINT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. 匿名树洞帖子表
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    author VARCHAR(50) NOT NULL,
    content VARCHAR(1000) NOT NULL,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    status TINYINT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 4. 每日健康记录表
CREATE TABLE IF NOT EXISTS user_health_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    record_date DATE NOT NULL,
    wake_early TINYINT DEFAULT 0,
    water_done TINYINT DEFAULT 0,
    fresh_veggies TINYINT DEFAULT 0,
    sleep_early TINYINT DEFAULT 0,
    water_ml INTEGER DEFAULT 0,
    steps INTEGER DEFAULT 0,
    focus_minutes INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, record_date)
);

-- 5. 身心趋势数据表
CREATE TABLE IF NOT EXISTS user_trend_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    record_date DATE NOT NULL,
    physical_score INTEGER DEFAULT 50,
    energy_score INTEGER DEFAULT 50,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, record_date)
);

-- 6. 食堂配餐建议表
CREATE TABLE IF NOT EXISTS meal_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_type VARCHAR(10) NOT NULL,
    icon VARCHAR(50),
    icon_color VARCHAR(50),
    tag VARCHAR(50),
    tag_class VARCHAR(100),
    title VARCHAR(100) NOT NULL,
    description VARCHAR(300),
    calories INTEGER,
    protein INTEGER,
    sort_order INTEGER DEFAULT 0,
    status TINYINT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 7. 运动课程表
CREATE TABLE IF NOT EXISTS sport_courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(300),
    img_url VARCHAR(255),
    img_alt VARCHAR(100),
    duration VARCHAR(10),
    intensity VARCHAR(20),
    intensity_class VARCHAR(100),
    participants VARCHAR(20),
    category VARCHAR(20) DEFAULT 'all',
    status TINYINT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 8. 勋章定义表
CREATE TABLE IF NOT EXISTS medals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    icon VARCHAR(50),
    description VARCHAR(200),
    sort_order INTEGER DEFAULT 0
);

-- 9. 用户勋章关联表
CREATE TABLE IF NOT EXISTS user_medals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    medal_id INTEGER NOT NULL,
    achieved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (medal_id) REFERENCES medals(id),
    UNIQUE(user_id, medal_id)
);

-- 10. 运动匹配表
CREATE TABLE IF NOT EXISTS sport_matches (
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
);

-- 11. 急救知识表
CREATE TABLE IF NOT EXISTS first_aid_resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(300),
    icon VARCHAR(50),
    bg_class VARCHAR(50),
    border_class VARCHAR(50),
    icon_class VARCHAR(50),
    icon_hover_class VARCHAR(50),
    title_class VARCHAR(50),
    desc_class VARCHAR(50),
    sort_order INTEGER DEFAULT 0,
    status TINYINT DEFAULT 1
);

-- 12. 常备药品分类表
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    icon VARCHAR(50),
    icon_bg VARCHAR(50),
    icon_color VARCHAR(50),
    tag VARCHAR(50),
    tag_class VARCHAR(50),
    sort_order INTEGER DEFAULT 0,
    status TINYINT DEFAULT 1
);

-- 13. 医疗设施表
CREATE TABLE IF NOT EXISTS medical_facilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(300),
    lat DECIMAL(10,6),
    lng DECIMAL(10,6),
    distance VARCHAR(20),
    walk_time VARCHAR(20),
    rating VARCHAR(5),
    type VARCHAR(30),
    tag VARCHAR(100),
    tag_class VARCHAR(100),
    tel VARCHAR(20),
    status TINYINT DEFAULT 1
);

-- 14. 帖子点赞记录表
CREATE TABLE IF NOT EXISTS post_likes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(post_id, user_id)
);

-- 15. 心情打卡记录表
CREATE TABLE IF NOT EXISTS mood_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    mood_type VARCHAR(20) NOT NULL,
    record_date DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, record_date)
);

-- ============================================
-- 索引
-- ============================================

CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id);
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status);
CREATE INDEX IF NOT EXISTS idx_articles_tag ON articles(tag);
CREATE INDEX IF NOT EXISTS idx_articles_status ON articles(status);
CREATE INDEX IF NOT EXISTS idx_articles_created_at ON articles(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_matches_created_at ON sport_matches(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_facilities_type ON medical_facilities(type);
