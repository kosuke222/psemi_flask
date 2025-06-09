import sqlite3

def delete_user_by_userid(userid):
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row

    # ユーザーIDが 'username' のユーザーを削除
    conn.execute("DELETE FROM users WHERE userid = ?", (userid,))
    conn.commit()
    conn.close()

    print(f"ユーザー '{userid}' は削除されました。")

# 使用例
delete_user_by_userid('admin')  # 'aa' というユーザーを削除
