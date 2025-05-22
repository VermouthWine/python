<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from datetime import datetime, timezone, timedelta
=======
from flask import Flask, render_template, request, redirect, url_for, session
>>>>>>> 7dd81ee9010f7e584d25caddb96635e5f34f2fb6
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import requests
<<<<<<< HEAD
import json
=======
>>>>>>> 7dd81ee9010f7e584d25caddb96635e5f34f2fb6

# 環境変数の読み込み
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Supabaseクライアントの作成
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Flaskの設定
app = Flask(__name__)
app.secret_key = "your_secret_key"  # セッション用のシークレットキー

<<<<<<< HEAD
# セッションの設定
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)  # 15分操作なしで自動ログアウト

# セッションの永続化を有効にする
@app.before_request
def before_request():
    session.permanent = True  # 永続的なセッション設定
    if 'user_id' in session:
        # セッションが存在している場合のみ更新
        session.modified = True

# セキュリティの強化設定
app.config['SESSION_COOKIE_SECURE'] = False     # HTTPSのみでクッキー送信 localhost環境のため一時false
app.config['SESSION_COOKIE_HTTPONLY'] = True   # JavaScriptからのアクセスを防止
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # クロスサイトのCSRF防止

# ホームページ (ログインかサインアップを選ぶ画面)
=======

# 🔹 ホームページ (ログインかサインアップを選ぶ画面)
>>>>>>> 7dd81ee9010f7e584d25caddb96635e5f34f2fb6
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

<<<<<<< HEAD
# サインアップページ & 処理
=======

# 🔹 サインアップページ & 処理
>>>>>>> 7dd81ee9010f7e584d25caddb96635e5f34f2fb6
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            # サインアップを実行
            user = supabase.auth.sign_up({"email": email, "password": password})
            print(f"サインアップ成功: {user}")
            # 確認リンクの送信完了メッセージを表示
            return render_template("signup.html", success=f"{email} に確認リンクが送信されました。")
        except Exception as e:
            print(f"サインアップ失敗: {e}")
            return render_template("signup.html", error="サインアップに失敗しました。")
    return render_template("signup.html")

<<<<<<< HEAD
# ログインページ & ログイン処理
=======

# 🔹 ログインページ & ログイン処理
>>>>>>> 7dd81ee9010f7e584d25caddb96635e5f34f2fb6
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if user.user.email_confirmed_at:
                # セッションにユーザーIDとメールアドレスを保存
                session['user_id'] = user.user.id
                session['user_email'] = user.user.email
                print(f"ログイン成功！ユーザーID: {email}")
                return redirect(url_for('dashboard'))
            else:
                return render_template("login.html", error="メールの確認が完了していません。")
        except Exception as e:
            print(f"ログイン失敗: {e}")
            return render_template("login.html", error="ログインに失敗しました。")
    return render_template("login.html")

<<<<<<< HEAD
# パスワードリセットリクエストページ（忘れた時）
@app.route("/password_reset_request", methods=["GET", "POST"])
def password_reset_request():
    message = None
    if request.method == "POST":
        email = request.form.get("email")
        access_token = request.args.get("access_token")
        try:
            response = supabase.auth.reset_password_for_email(
                email,
                {
                    "redirectTo": "http://localhost:5000/password_reset_redirect"
                }
            )
            print(f"パスワードリセットメール送信成功: {response}")
            message = f"{email} にパスワードリセット用のメールを送信しました。"
        except Exception as e:
            print(f"パスワードリセットメール送信失敗: {e}")
            message = "メール送信に失敗しました。メールアドレスを確認してください。"

    return render_template("password_reset_request.html", message=message)


@app.route("/password_reset_redirect")
def password_reset_redirect():
    # 中間ページ。JavaScriptでハッシュからクエリに変換しリダイレクトするだけ
    return render_template("password_reset_redirect.html")



@app.route("/password_reset_form", methods=["GET", "POST"])
def password_reset_form():
    access_token = request.args.get("access_token")
    type_ = request.args.get("type")

    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not new_password or not confirm_password:
            return render_template("password_reset_form.html", error="すべての項目を入力してください。", access_token=access_token, type=type_)

        if new_password != confirm_password:
            return render_template("password_reset_form.html", error="パスワードが一致しません。", access_token=access_token, type=type_)

        try:
            # リカバリトークンでセッション確立
            login_response = requests.post(
                f"{SUPABASE_URL}/auth/v1/token?grant_type=recovery",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Content-Type": "application/json"
                },
                json={"token": access_token}
            )
            login_response.raise_for_status()
            tokens = login_response.json()
            jwt = tokens["access_token"]

            # JWT でパスワードを更新
            update_response = requests.put(
                f"{SUPABASE_URL}/auth/v1/user",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {jwt}",
                    "Content-Type": "application/json"
                },
                json={"password": new_password}
            )
            update_response.raise_for_status()

            return redirect(url_for("login", message="パスワードが更新されました。ログインしてください。"))
        except Exception as e:
            print("パスワード更新失敗:", e)
            return render_template("password_reset_form.html", error="パスワード更新に失敗しました。", access_token=access_token, type=type_)

    return render_template("password_reset_form.html", access_token=access_token, type=type_)


# メール変更ページ & 処理
@app.route("/change_email", methods=["GET", "POST"])
def change_email():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == "GET":
        access_token = request.args.get("access_token")
        return render_template("change_email.html", access_token=access_token)

    if request.method == "POST":
        new_email = request.form.get("new_email")
        access_token = request.form.get("access_token")

        if not access_token or not new_email:
            return render_template("change_email.html", error="必要な情報が不足しています。", access_token=access_token)

        supabase_with_token = create_client(SUPABASE_URL, SUPABASE_KEY)
        supabase_with_token.auth.session = {
            "access_token": access_token,
            "token_type": "bearer"
        }

        try:
            response = supabase_with_token.auth.update_user({
                "email": new_email
            })
            return render_template("change_email.html", success="確認メールを送信しました。新しいアドレスで確認してください。", access_token=access_token)
        except Exception as e:
            print("メール変更エラー:", e)
            return render_template("change_email.html", error="メールアドレスの変更に失敗しました。", access_token=access_token)


# 共通関数: Supabaseからデータを取得する
def get_supabase_data(table_name, user_id, exclude_fields=None):
    try:
        query = supabase.table(table_name).select("*").eq("user_id", user_id)
        response = query.execute()
        if exclude_fields:
            # 除外フィールドを削除
            for row in response.data:
                for field in exclude_fields:
                    row.pop(field, None)
        return response.data
    except Exception as e:
        print(f"データ取得エラー: {e}")
        return []

    try:
        response = supabase.table(table_name).select("*").eq("user_id", user_id).execute()
        print(f"{table_name} 取得結果:", response.data)

        if response.data and len(response.data) > 0:
            return {
                key: value for key, value in response.data[0].items()
                if key not in exclude_fields and value
            }
        else:
            return None
    except Exception as e:
        print(f"{table_name} 取得エラー:", e)
        return None

# ダッシュボード（ログイン後のページ）
@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_email = session.get('user_email')

    tables = {
        "profile": "profile",
        "skillsheet": "skillsheet",
    }

    data = {}
    for table_name, var_name in tables.items():
        data[var_name] = get_supabase_data(table_name, user_id)

    try:
        response = supabase.table("project").select("*").eq("user_id", user_id).execute()
        print("project 取得結果:", response.data)
        projects = response.data if response.data else []
    except Exception as e:
        print("project 取得エラー:", e)
        projects = []

    return render_template(
        "dashboard.html",
        user_id=user_id,
        user_email=user_email,
        profile=data["profile"],
        skillsheet=data["skillsheet"],
        projects=projects
    )

# プロフィール入力処理
@app.route("/profile_input", methods=["GET", "POST"])
def profile_input():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        last_name = request.form.get("last_name")
        first_name = request.form.get("first_name")
        age = request.form.get("age")
        location = request.form.get("location")
        occupation = request.form.get("occupation")
        education = request.form.get("education")
        certifications = request.form.get("certifications")
        bio = request.form.get("bio")

        try:
            result = supabase.table("profile").upsert({
                "user_id": session['user_id'],
                "name": name,
                "age": age,
                "location": location,
                "occupation": occupation,
                "education": education,
                "certifications": certifications,
                "bio": bio,
                "initial": initial,  # イニシャルを追加
            }, on_conflict=["user_id"]).execute()

            if result.model_dump().get("error"):
                print("保存エラー:", result.error)
                return render_template("profile_input.html", error="保存に失敗しました。")

            return redirect(url_for("dashboard"))

        except Exception as e:
            print(f"エラー: {e}")
            return render_template("profile_input.html", error="予期せぬエラーが発生しました。")

    user_id = session['user_id']
    profile_data = get_supabase_data("profile", user_id) or {}
    return render_template("profile_input.html", profile=profile_data)

# スキルシート作成ページ & 処理
@app.route("/skillsheet_input", methods=["GET", "POST"])
def skillsheet_input():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    categories = {
        "プログラミング言語": ["python", "ruby", "javascript", "shell", "c", "c++", "c#", "java", "html", "go", "css", "swift", "kotlin", "sql"],
        "フレームワーク": ["flask", "rails", "vue", "react", "express", "springboot", "django", "nextjs", "nuxt", "svelte"],
        "ミドルウェア": ["nginx", "apache", "mysql", "postgresql", "redis", "mongodb", "elasticsearch", "rabbitmq", "docker", "kubernetes", "terraform", "prometheus", "grafana", "fluentd"],
        "インフラ": ["aws", "azure", "gcp", "oci", "linux", "windows", "vmware", "hyper-v", "ansible", "chef", "puppet", "jenkins", "gitlabci", "circleci", "githubactions", "terraform"]
    }

    if request.method == "POST":
        skillsheet_data = {}
        for category, skills in categories.items():
            for skill in skills:
                skillsheet_data[skill] = True if request.form.get(skill) == "on" else False

        try:
            result = supabase.table("skillsheet").upsert(
                {"user_id": session['user_id'], **skillsheet_data},
                on_conflict=["user_id"]
            ).execute()

            if result.model_dump().get("error"):
                return render_template("skillsheet_input.html", categories=categories, error="保存に失敗しました。")

            return redirect(url_for("dashboard"))

        except Exception as e:
            print(f"スキル保存エラー: {e}")
            return render_template("skillsheet_input.html", categories=categories, error="予期せぬエラーが発生しました。")

    # GET時は既存データ取得
    skillsheet_data = get_supabase_data("skillsheet", session['user_id']) or {}
    return render_template("skillsheet_input.html", categories=categories, skillsheet=skillsheet_data)

# プロジェクト入力処理
@app.route("/project_input", methods=["GET", "POST"])
def project_input():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        project_name = request.form.get("project_name")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        role = request.form.get("role")
        responsibilities = request.form.get("responsibilities")
        achievements = request.form.get("achievements")
        tools = request.form.get("tools")
        technologies = request.form.get("technologies")

        try:
            result = supabase.table("project").insert([{
                "user_id": session['user_id'],
                "project_name": project_name,
                "start_date": start_date,
                "end_date": end_date,
                "role": role,
                "responsibilities": responsibilities,
                "achievements": achievements,
                "tools": tools,
                "technologies": technologies,
            }]).execute()

            if result.model_dump().get("error"):
                return render_template("project_input.html", error="保存に失敗しました。")

            return redirect(url_for("dashboard"))

        except Exception as e:
            print(f"プロジェクト保存エラー: {e}")
            return render_template("project_input.html", error="予期せぬエラーが発生しました。")

    return render_template("project_input.html")

# ログアウト処理
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
=======

# 🔹 ダッシュボード（ログイン後のページ）
@app.route("/dashboard")
def dashboard():
    if 'user_id' in session:
        return render_template("dashboard.html", user_id=session['user_id'], user_email=session['user_email'])
    else:
        return redirect(url_for('login'))


# 🔹 スキルシート作成ページ
@app.route("/skillsheet_input")
def skillsheet_input():
    return render_template("skillsheet_input.html")


# 🔹 ログアウト処理
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))


# アプリの実行
if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 7dd81ee9010f7e584d25caddb96635e5f34f2fb6
