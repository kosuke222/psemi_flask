from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, template_folder="templates")


# ---------------- データベース接続 ------------------
def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    # usersテーブルのみを作成します
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT UNIQUE NOT NULL,
            pwd TEXT NOT NULL,
            super INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# ---------------- ルーティング ------------------
@app.route('/') # これを追加/修正
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        userid = request.form.get('userid', '').strip()
        pwd = request.form.get('pwd', '').strip()

        if not userid or not pwd:
            error_message = "⚠ ユーザーIDとパスワードを入力してください。"
            return render_template('login.html', error_message=error_message)

        conn = get_db_connection()
        # 注意: このSQLクエリはSQLインジェクションの脆弱性を含んでいます。
        # 教育目的のため、元のコードの記述を維持しています。
        # 実際の本番環境では、プレースホルダを使用した安全なクエリを使用してください。
        sql = f"SELECT id, userid, super FROM users WHERE userid = '{userid}' AND pwd = '{pwd}'"
        user = conn.execute(sql).fetchone()
        conn.close()

        if user:
            # ログイン成功時は、セッションやクッキーを使用せず、ログイン成功ページにリダイレクトします。
            return redirect(url_for('login_success'))
        else:
            error_message = 'ユーザーIDまたはパスワードが違います。'

    return render_template('login.html', error_message=error_message)

@app.route('/login_success')
def login_success():
    """
    ログイン成功時に表示されるページ。
    """
    return render_template('login_success.html')

@app.route('/register', methods=['POST'])
def register():
    userid = request.form.get("userid")
    pwd = request.form.get("pwd")

    conn = get_db_connection()
    sql = "INSERT INTO users (userid, pwd) VALUES (?, ?)"
    try:
        conn.execute(sql, (userid, pwd))
        conn.commit()
    except sqlite3.IntegrityError:
        return "ユーザーIDが既に存在します"
    finally:
        conn.close()

    # ユーザー登録後はログインページへリダイレクト
    return redirect(url_for("login"))

# ---------------- メイン ------------------
if __name__ == "__main__":
    with app.app_context():
        create_tables() # アプリケーション起動時にusersテーブルを作成
    app.run(debug=True)