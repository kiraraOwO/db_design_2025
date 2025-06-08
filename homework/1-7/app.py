from flask import Flask, request, render_template, session, redirect
import db_

app = Flask(__name__)
app.secret_key = "BtdV2KNuMQj7gf0YX3tIUjNm4X4RfnCn"

@app.route("/")
def index():
    data = db_.get_articles(limited=-1, preview=True)
    # page = request.args.get("p", default=1, type=int)
    if "user_id" in session:
        return render_template("index.html", articles=data, login=True, nickname=session["nickname"])
    else:
        return render_template("index.html", articles=data, login=False)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", success=False)
    if request.method == "POST":
        input_email = request.form.get("email")
        input_password = request.form.get("password")
        if not input_email or not input_password:
            return render_template("login.html", success=False, msg="pls input the input.")
        do = db_.auth(input_email, input_password)
        print(do)
        if do["status"] == 0:
            session["user_id"] = do["id"]
            session["nickname"] = do["msg"]
            return render_template("login.html", success=True, nickname=do["msg"])
        return render_template("login.html", success=False, msg="email or password incorrect.")

@app.route("/logout")
def logout():
    if "user_id" not in session:
        return render_template("redirect.html", msg="you should login first.", url="/")
    session.pop('user_id', None)
    session.pop('nickname', None)
    return render_template("redirect.html", msg="bye.", url="/")

@app.route("/article", strict_slashes=False)
@app.route("/article/<int:article_id>")
def article_read(article_id=None):
    if not article_id:
        return redirect("/")
    do = db_.get_articles(article_id=article_id)
    print(do)
    if do:
        return render_template("article.html", data=do[0])
    else:
        return "<p>article not found</p><a href='/'>home</a>", 404

@app.route("/user")
def user():
    if "user_id" not in session:
        return redirect("/login")
    do = db_.get_articles(user_id=session["user_id"], preview=True)
    return render_template("user.html", articles=do, login=True, nickname=session["nickname"])


@app.route("/edit", methods=["GET", "POST"], strict_slashes=False)
@app.route("/edit/<int:article_id>", methods=["GET", "POST"])
def article_edit(article_id=None):
    if not article_id:
        return redirect("/")
    if "user_id" not in session:
        return redirect("/login")
    do = db_.get_articles(article_id=article_id)
    if not do:
        return render_template("redirect.html", msg="403", url="/user"), 403
    if do[0]["user_id"] != session["user_id"]:
        return render_template("redirect.html", msg="403", url="/user"), 403

    if request.method == "GET":
        return render_template("edit.html", data=do[0])
    if request.method == "POST":
        input_title = request.form.get("title")
        input_content = request.form.get("content")
        if not input_title or not input_content:
            return "pls check your input.", 400
        if len(input_title) > 40:
            return "title max len 40", 400
        do = db_.article_update(article_id=article_id, title=input_title, content=input_content)
        if do == 0:
            return render_template("redirect.html", msg="ok", url="/user")
        return "e", 400

    return "?", 500

@app.route("/edit/new", methods=["GET", "POST"])
def article_create():
    if "user_id" not in session:
        return redirect("/login")
    if request.method == "GET":
        return render_template("edit.html", new=True)
    if request.method == "POST":
        input_title = request.form.get("title")
        input_content = request.form.get("content")
        if not input_title or not input_content:
            return "pls check your input.", 400
        if len(input_title) > 40:
            return "title max len 40", 400
        do = db_.article_insert(user_id=session["user_id"], title=input_title, content=input_content)
        if do == 0:
            return render_template("redirect.html", msg="ok", url="/user")
        return "e", 400

@app.route("/search", methods=["GET", "POST"])
def article_search():
    if request.method == "GET":
        return redirect("/")
    if request.method == "POST":
        input_keyword = request.form.get("keyword").strip()
        if not input_keyword:
            return "", 204
        do = db_.article_search(input_keyword)
        if "user_id" in session:
            return render_template("search.html", articles=do, login=True, keyword=input_keyword, nickname=session["nickname"])
        else:
            return render_template("search.html", articles=do, login=False, keyword=input_keyword)
    return "?", 500

@app.route("/del", methods=["GET", "POST"])
@app.route("/del/<int:article_id>", methods=["GET", "POST"])
def article_delete(article_id=None):
    if not article_id:
        return redirect("/")
    if "user_id" not in session:
        return redirect("/login")
    do = db_.get_articles(article_id=article_id)
    if not do:
        return render_template("redirect.html", msg="403", url="/user"), 403
    if do[0]["user_id"] != session["user_id"]:
        return render_template("redirect.html", msg="403", url="/user"), 403

    if request.method == "GET":
        return render_template("del.html", article=do[0])
    if request.method == "POST":
        do = db_.article_delete(article_id)
        if do == 0:
            return render_template("redirect.html", msg="deleted.", url="/user")
        else:
            return render_template("redirect.html", msg="err", url="/user"), 400
    return "?", 500

if __name__ == '__main__':
    app.run(debug=True, port=8081)
