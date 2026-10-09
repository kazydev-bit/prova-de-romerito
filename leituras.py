from flask import Blueprint, flash, redirect, render_template, request, session, url_for

import database
from seguranca import exigir_login


leituras_bp = Blueprint("leituras", __name__)


@leituras_bp.route("/leituras")
def index():
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    leituras = database.listar_leituras()
    return render_template("leituras.html", leituras=leituras)


@leituras_bp.route("/leituras/nova", methods=["GET", "POST"])
def nova_leitura():
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        paginas = int(request.form["paginas"])
        database.criar_leitura(titulo, autor, paginas)
        flash("Leitura cadastrada.")
        return redirect(url_for("leituras.index"))

    return render_template("nova_leitura.html")


@leituras_bp.route("/leituras/<int:leitura_id>/editar", methods=["GET", "POST"])
def editar_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    leitura = database.buscar_leitura(leitura_id)
    if leitura is None:
        return "Leitura não encontrada", 404

    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        paginas = int(request.form["paginas"])
        database.atualizar_leitura(leitura_id, titulo, autor, paginas)
        flash("Leitura atualizada.")
        return redirect(url_for("leituras.index"))

    return render_template("editar_leitura.html", leitura=leitura)


@leituras_bp.post("/leituras/<int:leitura_id>/concluir")
def concluir_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    database.alternar_concluida(leitura_id)
    flash("Status da leitura atualizado.")
    return redirect(url_for("leituras.index"))


@leituras_bp.post("/leituras/<int:leitura_id>/excluir")
def excluir_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    database.excluir_leitura(leitura_id)
    flash("Leitura excluída.")
    return redirect(url_for("leituras.index"))
