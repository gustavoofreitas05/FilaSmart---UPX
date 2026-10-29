from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from pathlib import Path
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("FILASMART_SECRET_KEY", "chave-local-apenas-para-desenvolvimento")
DB = Path(__file__).with_name("filasmart.db")

def connect():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; c.execute("PRAGMA foreign_keys=ON"); return c

def init_db():
    with connect() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, role TEXT NOT NULL CHECK(role IN ('customer','owner')), created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS services(id INTEGER PRIMARY KEY, owner_id INTEGER NOT NULL REFERENCES users(id), name TEXT NOT NULL, description TEXT DEFAULT '', active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS queue_entries(id INTEGER PRIMARY KEY, service_id INTEGER NOT NULL REFERENCES services(id), user_id INTEGER NOT NULL REFERENCES users(id), status TEXT NOT NULL DEFAULT 'waiting' CHECK(status IN ('waiting','called','serving','completed','cancelled')), joined_at TEXT NOT NULL, called_at TEXT, completed_at TEXT);
        CREATE INDEX IF NOT EXISTS queue_idx ON queue_entries(service_id,status,joined_at);
        """)

def me():
    if not session.get("user_id"): return None
    with connect() as c: return c.execute("SELECT id,name,email,role FROM users WHERE id=?", (session["user_id"],)).fetchone()

@app.context_processor
def ctx(): return {"logged_user":me()}

def login_required(fn):
    @wraps(fn)
    def w(*a,**kw):
        if not me(): flash("Entre na sua conta para continuar.","error"); return redirect(url_for("login"))
        return fn(*a,**kw)
    return w

def role_required(role):
    def deco(fn):
        @wraps(fn)
        def w(*a,**kw):
            u=me()
            if not u: return redirect(url_for("login"))
            if u["role"]!=role: abort(403)
            return fn(*a,**kw)
        return w
    return deco

@app.route("/")
def index():
    with connect() as c:
        services=c.execute("""SELECT s.*,u.name business_name,(SELECT COUNT(*) FROM queue_entries q WHERE q.service_id=s.id AND q.status='waiting') waiting_count FROM services s JOIN users u ON u.id=s.owner_id WHERE s.active=1 ORDER BY s.id DESC""").fetchall()
    return render_template("index.html",services=services)

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form.get("name","").strip(); email=request.form.get("email","").strip().lower(); pw=request.form.get("password",""); role=request.form.get("role","customer")
        if not name or not email or len(pw)<8 or role not in ("customer","owner"):
            flash("Preencha os campos. A senha precisa ter ao menos 8 caracteres.","error")
        else:
            try:
                with connect() as c: c.execute("INSERT INTO users(name,email,password_hash,role,created_at) VALUES(?,?,?,?,?)",(name,email,generate_password_hash(pw),role,datetime.now().isoformat(timespec="seconds")))
                flash("Conta criada. Faça login.","success"); return redirect(url_for("login"))
            except sqlite3.IntegrityError: flash("E-mail já cadastrado.","error")
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        with connect() as c: u=c.execute("SELECT * FROM users WHERE email=?",(request.form.get("email","").strip().lower(),)).fetchone()
        if u and check_password_hash(u["password_hash"],request.form.get("password","")):
            session.clear(); session["user_id"]=u["id"]; return redirect(url_for("owner") if u["role"]=="owner" else url_for("my_queues"))
        flash("E-mail ou senha inválidos.","error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear(); return redirect(url_for("index"))

@app.route("/owner")
@login_required
@role_required("owner")
def owner():
    u=me()
    with connect() as c:
        services=c.execute("""SELECT s.*,(SELECT COUNT(*) FROM queue_entries q WHERE q.service_id=s.id AND q.status='waiting') waiting_count,(SELECT COUNT(*) FROM queue_entries q WHERE q.service_id=s.id AND q.status='completed') completed_count FROM services s WHERE s.owner_id=? ORDER BY s.id DESC""",(u["id"],)).fetchall()
        entries=c.execute("""SELECT q.*,u.name customer_name,s.name service_name FROM queue_entries q JOIN users u ON u.id=q.user_id JOIN services s ON s.id=q.service_id WHERE s.owner_id=? AND q.status IN ('waiting','called','serving') ORDER BY q.joined_at""",(u["id"],)).fetchall()
    return render_template("owner.html",services=services,entries=entries)

@app.route("/services/create",methods=["POST"])
@login_required
@role_required("owner")
def create_service():
    name=request.form.get("name","").strip(); desc=request.form.get("description","").strip()
    if name:
        with connect() as c: c.execute("INSERT INTO services(owner_id,name,description,created_at) VALUES(?,?,?,?)",(me()["id"],name,desc,datetime.now().isoformat(timespec="seconds")))
        flash("Serviço salvo no banco.","success")
    else: flash("Informe o nome do serviço.","error")
    return redirect(url_for("owner"))

@app.route("/services/<int:sid>/toggle",methods=["POST"])
@login_required
@role_required("owner")
def toggle(sid):
    with connect() as c:
        s=c.execute("SELECT * FROM services WHERE id=? AND owner_id=?",(sid,me()["id"])).fetchone()
        if not s: abort(404)
        c.execute("UPDATE services SET active=? WHERE id=?",(0 if s["active"] else 1,sid))
    return redirect(url_for("owner"))

@app.route("/services/<int:sid>/join",methods=["POST"])
@login_required
@role_required("customer")
def join(sid):
    u=me()
    with connect() as c:
        s=c.execute("SELECT id FROM services WHERE id=? AND active=1",(sid,)).fetchone()
        if not s: flash("Serviço indisponível.","error")
        elif c.execute("SELECT id FROM queue_entries WHERE service_id=? AND user_id=? AND status IN ('waiting','called','serving')",(sid,u["id"])).fetchone(): flash("Você já está nessa fila.","error")
        else:
            c.execute("INSERT INTO queue_entries(service_id,user_id,status,joined_at) VALUES(?,?,'waiting',?)",(sid,u["id"],datetime.now().isoformat(timespec="seconds")))
            flash("Entrada registrada na fila.","success")
    return redirect(url_for("my_queues"))

@app.route("/my-queues")
@login_required
@role_required("customer")
def my_queues():
    with connect() as c:
        rows=c.execute("""SELECT q.*,s.name service_name,u.name business_name FROM queue_entries q JOIN services s ON s.id=q.service_id JOIN users u ON u.id=s.owner_id WHERE q.user_id=? ORDER BY q.id DESC""",(me()["id"],)).fetchall()
        entries=[]
        for r in rows:
            d=dict(r)
            d["position"]=c.execute("SELECT COUNT(*) FROM queue_entries WHERE service_id=? AND status='waiting' AND joined_at<=?",(r["service_id"],r["joined_at"])).fetchone()[0] if r["status"]=="waiting" else None
            entries.append(d)
    return render_template("my_queues.html",entries=entries)

@app.route("/queue/<int:eid>/cancel",methods=["POST"])
@login_required
@role_required("customer")
def cancel(eid):
    with connect() as c: cur=c.execute("UPDATE queue_entries SET status='cancelled' WHERE id=? AND user_id=? AND status='waiting'",(eid,me()["id"]))
    flash("Você saiu da fila." if cur.rowcount else "Não foi possível cancelar a entrada.","success" if cur.rowcount else "error")
    return redirect(url_for("my_queues"))

@app.route("/queue/<int:eid>/action",methods=["POST"])
@login_required
@role_required("owner")
def action(eid):
    a=request.form.get("action"); trans={"call":("waiting","called","called_at"),"serve":("called","serving",None),"complete":("serving","completed","completed_at")}
    if a not in trans: abort(400)
    old,new,stamp=trans[a]
    with connect() as c:
        e=c.execute("SELECT q.*,s.owner_id FROM queue_entries q JOIN services s ON s.id=q.service_id WHERE q.id=?",(eid,)).fetchone()
        if not e or e["owner_id"]!=me()["id"]: abort(404)
        if e["status"]!=old: flash("Status mudou; atualize a página.","error")
        elif stamp: c.execute(f"UPDATE queue_entries SET status=?,{stamp}=? WHERE id=?",(new,datetime.now().isoformat(timespec="seconds"),eid))
        else: c.execute("UPDATE queue_entries SET status=? WHERE id=?",(new,eid))
    return redirect(url_for("owner"))

@app.route("/health")
def health():
    with connect() as c: c.execute("SELECT 1").fetchone()
    return {"status":"ok","database":"connected"}

init_db()

if __name__=="__main__":
    app.run(debug=True)
