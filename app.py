from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from funcions import calcul2, crear_pdf
from math import atan

# Configure application
app = Flask(__name__)

# Configure session to use filesystem
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["rampa_h"] = None
app.config["rampa_l"] = None
app.config["rampa_x"] = None
app.config['entrades_rampa_ok'] = False
app.config['entrades_cotxe_ok'] = False
app.config["cotxe_b"] = None
app.config["cotxe_p"] = None
app.config["cotxe_ec"] = None
app.config["cotxe_m"] = None
app.config["cotxe_h"] = None
app.config["cotxe_a "] = None
app.config["cotxe_ms"] = None
Session(app)

# rampa_h = 0
# rampa_l = 0
# rampa_x = 0
cotxe_p = 0
cotxe_ec = 0
cotxe_m = 0
cotxe_h = 0
cotxe_a = 0
cotxe_b = 0
cotxe_ms = 0
llista_p = []


@app.route("/", methods=["GET", "POST"])
def index():
    """plana presentacio"""
    if request.method == "POST":
        if request.form.get('rampa') == 'rampa':
            return redirect('rampa')
        if request.form.get('cotxe') == 'cotxe':
            return redirect('cotxe')
    return render_template("index.html")


@app.route("/rampa", methods=["GET", "POST"])
def rampa():
    flash('Si canvies alguna mida no oblidis validar')
    if request.method == "POST":
        # borrar els valors de la rampa
        if request.form.get('borrar') == "borra":
            flash('borrades')
            session['rampa_x'] = None
            session['rampa_l'] = None
            session['rampa_h'] = None
            session['entrades_rampa_ok'] = False
            return render_template("rampa.html")
        try:
            session['rampa_h'] = int(request.form.get("h"))
            session['rampa_l'] = int(request.form.get("l"))
            session['rampa_x'] = int(request.form.get("x"))
            session['entrades_rampa_ok'] = True
            return redirect("cotxe")
        except Exception:
            session['rampa_h'] = request.form.get("h")
            session['rampa_l'] = request.form.get("l")
            session['rampa_x'] = request.form.get("x")
            session['entrades_rampa_ok'] = False
            session["calcul"] = [(0, 0, 0)]
            flash('Falten entrar dades')
            return render_template("rampa.html")

    else:  # si ve de get
        return render_template("rampa.html")


@app.route("/cotxe", methods=["GET", "POST"])
def cotxe():
    flash('Si canvies alguna mida no oblidis validar')
    if request.method == "POST":
        if request.form.get('borrar') == "borra":
            flash('borrada la sessio')
            session["cotxe_b"] = None
            session["cotxe_p"] = None
            session["cotxe_ec"] = None
            session["cotxe_m"] = None
            session["cotxe_h"] = None
            session["cotxe_a"] = None
            session["cotxe_ms"] = None
            session["ret"] = None
            session['entrades_cotxe_ok'] = False
            return render_template("cotxe.html")

        if request.form.get('validar') == "validar":
            try:
                session["cotxe_b"] = int(request.form.get('b'))
                session["cotxe_p"] = int(request.form.get('p'))
                session["cotxe_ec"] = int(request.form.get('ec'))
                session["cotxe_m"] = int(request.form.get('m'))
                session["cotxe_h"] = int(request.form.get('h'))
                session["cotxe_a"] = int(request.form.get('a'))
                session["cotxe_ms"] = int(request.form.get('ms'))
                session['entrades_cotxe_ok'] = True
                session['resultats'] = [(0, 0, 0)]
                return redirect("resultats")
            except Exception:
                session["cotxe_b"] = request.form.get('b')
                session["cotxe_p"] = request.form.get('p')
                session["cotxe_ec"] = request.form.get('ec')
                session["cotxe_m"] = request.form.get('m')
                session["cotxe_h"] = request.form.get('h')
                session["cotxe_a"] = request.form.get('a')
                session["cotxe_ms"] = request.form.get('ms')
                session['entrades_cotxe_ok'] = False
                flash(' Falten dades')
                return render_template("cotxe.html")
    else:  # be de get
        return render_template("cotxe.html")


@app.route("/resultats", methods=["GET", "POST"])
def resultats():
    if request.method == "POST":
        if request.form.get('download') == "download":
            nom = request.form.get("nom")
            autor = request.form.get("autor")
            # crear el pdf
            crear_pdf(nom, autor, session['calcul'])
            flash("informe creat")
        if request.form.get('calcular') == "calcular":
            # calcular
            ret = calculs_resultats()
            if ret == 0:
                flash("No es pot fer la rampa")
                return redirect("/rampa")
            if ret == 1:
                flash(" No cal modificar la rampa original")
                ret = [(1, session['rampa_l'], session['rampa_h'])]
                return render_template("resultats.html", ret=ret)
            if ret == 2:
                flash("hi ha dades entrades erronies")
                return redirect("/rampa")
            return render_template('resultats.html', ret=ret)
    else:
        flash("clicar calcular per obtenir les dades")
        if not session['entrades_cotxe_ok']:
            flash('falten entrar dades del cotxe')
            return redirect('cotxe')
        if not session['entrades_rampa_ok']:
            flash('Falten entrar dades de la rampa')
            return redirect('rampa')
        return render_template('resultats.html')
    return render_template('resultats.html')


def calculs_resultats():
    try:
        rampa_x = int(session['rampa_x'])
        rampa_l = int(session['rampa_l'])
        rampa_h = int(session['rampa_h'])
        cotxe_b = int(session["cotxe_b"])
        cotxe_ec = int(session["cotxe_ec"])
        cotxe_p = int(session["cotxe_p"])
        cotxe_m = int(session["cotxe_m"])
        cotxe_h = int(session["cotxe_h"])
        cotxe_a = int(session["cotxe_a"])
        cotxe_ms = int(session["cotxe_ms"])
        session["calcul"] = [(0, 0, 0)]
    except Exception:
        ret = 2
        return ret

    if session['entrades_cotxe_ok'] & session['entrades_rampa_ok']:
        a_max_morro = atan((cotxe_a - cotxe_ms) / cotxe_m)
        a_max_centre = 2 * atan((cotxe_h - cotxe_ms) / (cotxe_ec / 2))
        a_max_cul = atan((cotxe_b - cotxe_ms) / cotxe_p)
        if a_max_cul < a_max_morro:
            a_max_morro = a_max_cul
            cotxe_m = cotxe_p
            cotxe_a = cotxe_b
        ret = calcul2(cotxe_ec, rampa_x, rampa_h, a_max_morro, a_max_centre,
                      cotxe_m, cotxe_a, cotxe_ms)
        session['calcul'] = ret
        return ret
