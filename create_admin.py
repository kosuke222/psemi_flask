import sqlite3

def create_admin_user():
    conn = sqlite3.connect('todo.db')

    existing = conn.execute("SELECT * FROM users WHERE userid = ?", ("admin",)).fetchone()
    if existing:
        print("ユーザー 'admin' はすでに存在します。")
    else:
        conn.execute("INSERT INTO users (userid, pwd, super) VALUES (?, ?, ?)", ("bob", "pass02", "4"))
        conn.commit()
        print("✅ 管理者ユーザー 'admin' を追加しました（パスワード: admin123）")

    conn.close()

create_admin_user()