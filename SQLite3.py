import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class BlogDB:
    def __init__(self, db_name: str = 'blog.db'):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('PRAGMA foreign_keys = ON')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
    def create_user(self, username: str) -> int:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username) VALUES (?)",
                (username,)
            )
            return cursor.lastrowid

    def create_post(self, user_id: int, title: str, content: str) -> int:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
                (user_id, title, content)
            )
            return cursor.lastrowid
    def  get_user_posts(self, username: str) -> List[Dict]:
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT posts.title, posts.content, posts.created_at
                FROM posts
                JOIN users ON posts.user_id = users.id
                WHERE users.username = ?
                ORDER BY posts.created_at DESC
            ''', (username,))
            return [dict(row) for row in cursor.fetchall()]

    def get_all_users(self) -> List[str]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users")
            return [row[0] for row in cursor.fetchall()]

if __name__ == "__main__":
    db = BlogDB()

    user1_id = db.create_user("python_dev")
    user2_id = db.create_user("js_lover")



    db.create_post(user1_id, "Зачем учить Python", "Python - отличный язык для начинающих...")
    db.create_post(user1_id, "SQLite в Python", "Модуль sqlite3 позволяет легко работать с БД...")
    db.create_post(user2_id, "React vs Vue", "Оба фреймворка имеют свои преимущества...")
    db.create_post(user1_id, "Але але", "Гизатулин")

    posts = db.get_user_posts("python_dev")
    print(f"\nПосты пользователя python_dev:")
    for post in posts:
        print(f"\n {post['title']}")
        print(f"   {post['content'][:50]}...")
        print(f"   {post['created_at']}")

    print(f"\nВсе пользователи: {','.join(db.get_all_users())}")