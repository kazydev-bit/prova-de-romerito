from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import sqlite3
import database


auth_bp = Blueprint("auth", __name__)


# A session do Flask precisa de uma chave secreta.
@auth_bp.record_once
def configurar_sessao(state):
    if not state.app.secret_key:
        state.app.secret_key = "ajuda_ai_romerito"


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.")
            return redirect(url_for("auth.registro"))

        if database.buscar_usuario_por_email(email):
            flash("Este e-mail já está cadastrado.")
            return redirect(url_for("auth.registro"))

        senha_hash = generate_password_hash(senha)

        try:
            database.criar_usuario(nome, email, senha_hash)
        except sqlite3.IntegrityError:
            flash("Não foi possível cadastrar. Verifique se o e-mail já existe.")
            return redirect(url_for("auth.registro"))

        flash("Cadastro realizado com sucesso. Faça login.")
        return redirect(url_for("auth.login"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not email or not senha:
            flash("Informe o e-mail e a senha.")
            return redirect(url_for("auth.login"))

        usuario = database.buscar_usuario_por_email(email)

        if usuario is None or not check_password_hash(usuario.senha_hash, senha):
            flash("E-mail ou senha incorretos.")
            return redirect(url_for("auth.login"))

        session.clear()
        session["usuario_id"] = usuario.id
        session["usuario_nome"] = usuario.nome

        flash("Login realizado com sucesso.")
        return redirect(url_for("leituras.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.")
    return redirect(url_for("auth.login"))