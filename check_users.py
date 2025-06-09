import sqlite3

def check_users():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    users = conn.execute("SELECT id, userid, pwd, super FROM users").fetchall()
    conn.close()

    print("登録済みユーザー：")
    for user in users:
        print(f"ID: {user['id']}, ユーザーID: {user['userid']}, パスワード: {user['pwd']}, 管理者: {user['super']}")

check_users()
