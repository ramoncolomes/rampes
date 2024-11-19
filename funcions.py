from sympy import Point, Segment, atan, cos, sin, solve, symbols
from flask import session, flash
from reportlab.pdfgen import canvas  # pdf
from reportlab.lib import colors
from datetime import date
import os

beta = symbols("beta")


def punt_sota(punt_inici, llargada_tram, angle_sota, n_punts_sota):  # si
    px = punt_inici.x + llargada_tram * cos(angle_sota * n_punts_sota)
    py = punt_inici.y + llargada_tram * sin(angle_sota * n_punts_sota)
    return Point(round(px), round(py))


def punt_sobre(punt_inici, llargada_tram, angle_sobre, n_punts_sobre):  # si
    px = punt_inici.x - llargada_tram * cos(angle_sobre * n_punts_sobre)
    py = punt_inici.y - llargada_tram * sin(angle_sobre * n_punts_sobre)
    return Point(round(px), round(py))


# tram minim
def tr_min2(h_morro, entre_eixos, morro, a_max_morro, marge_seg, beta):
    h_morro_calcul = h_morro - marge_seg
    morroentreeixos = morro + entre_eixos
    lt = (h_morro_calcul ** 2 + morroentreeixos ** 2) ** 0.5

    l_morro = (morro ** 2 + h_morro_calcul ** 2) ** 0.5
    alfa = a_max_morro
    sin2alfambeta = sin(2 * alfa) * cos(beta) - cos(2 * alfa) * sin(beta)
    tt1 = sin2alfambeta * entre_eixos / sin(alfa)
    sinbetamalfa = sin(beta) * cos(alfa) - cos(beta) * sin(alfa)
    tt2 = sinbetamalfa * entre_eixos / sin(alfa)
    tt3 = tt1 - tt2
    tt4 = sinbetamalfa * l_morro / sin(alfa)
    eq = tt1 * cos(alfa) + tt2 * cos(2 * alfa) + tt3 * cos(2 * alfa) + tt4 * cos(3 * alfa) - lt * cos(beta)
    b = solve(eq, beta)
    t1 = round(tt1.replace(beta, b[0]))
    t2 = int(t1 / 10) * 10 + 10
    return t2


def calcul2(entre_eixos, planta_rampa, h_final, a_max_morro, a_max_centre, morro, h_morro, marge_seg):
    tram_min2 = tr_min2(h_morro, entre_eixos, morro, a_max_morro, marge_seg, beta)
    llargada_tram = entre_eixos + 10
    llista_p_sota = [Point(-entre_eixos, 0), Point(0, 0)]
    llista_p_sobre = [Point(int(planta_rampa) + int(entre_eixos), h_final), Point(planta_rampa, h_final)]
    insertar_sota = True
    solucio = False
    pendent_enllas = Segment(llista_p_sota[-1], llista_p_sobre[-1]).slope

    if pendent_enllas <= a_max_morro and pendent_enllas <= a_max_centre:
        return 1  # la rampa original ja serveix
    # inici bucle calcul
    while not solucio:
        pendent_enllas = Segment(llista_p_sota[-1], llista_p_sobre[-1]).slope
        pend_sota = Segment(llista_p_sota[-1], llista_p_sota[-2]).slope
        pend_sobre = Segment(llista_p_sobre[-1], llista_p_sobre[-2]).slope
        if pendent_enllas > pend_sota:  # triar morro
            angle_inf = False
        else:
            angle_inf = True
            insertar_sota = False
        if pendent_enllas > pend_sobre:
            angle_sup = False
        else:
            angle_sup = True
        if not angle_inf and insertar_sota:  # insertar punt sota perque el pendent es false
            # insertar punt sota
            pnt = punt_sota(llista_p_sota[-1], llargada_tram, a_max_morro, len(llista_p_sota) - 1)
            llista_p_sota.append(pnt)
            insertar_sota = False
        elif not angle_sup and not insertar_sota:
            # insertar punt sobre
            pnt = punt_sobre(llista_p_sobre[-1], llargada_tram, a_max_centre, len(llista_p_sobre) - 1)
            llista_p_sobre.append(pnt)
            insertar_sota = True
        else:
            # solucio = True  # rampa original ja serveix
            llarg = round((planta_rampa ** 2 + h_final ** 2) ** 0.5)
            flash('rampa original ja serveix')
            return [(1, h_final, llarg)]
        # si no es posible  començar de nou
        if llista_p_sota[-1].x > llista_p_sobre[-1].x or llista_p_sota[-1].y > llista_p_sobre[-1].y:
            # si es creuen les rampes disminuir llargada i recalcular
            llargada_tram -= 100

            if llargada_tram < tram_min2:
                return 0  # no es pot fer la rampa

            llista_p_sota = [Point(-entre_eixos, 0), Point(0, 0)]
            llista_p_sobre = [Point(planta_rampa + entre_eixos, h_final), Point(planta_rampa, h_final)]
            insertar_sota = True

        else:
            pendent_enllas = Segment(llista_p_sota[-1], llista_p_sobre[-1]).slope
            angle_enllas = atan(pendent_enllas)
            pend_sota = Segment(llista_p_sota[-1], llista_p_sota[-2]).slope
            angle_sota_enllas = atan(pend_sota)
            pend_sobre = Segment(llista_p_sobre[-1], llista_p_sobre[-2]).slope
            angle_sobre_enllas = atan(pend_sobre)

            if angle_enllas - angle_sota_enllas < a_max_morro and angle_enllas - angle_sobre_enllas < a_max_centre:
                solucio = True

    # organitzar la sortida per imprimir a pantalla
    llista_p_sota.reverse()
    llp = llista_p_sobre + llista_p_sota
    llp.pop()
    llp.pop(0)
    resp = []

    for i, l in enumerate(llp):
        if i < len(llp) - 1:
            l1 = int(Segment(Point(llp[i + 1]), Point(llp[i])).length)
            h = round(h_final - llp[i + 1].y)
            resp.append((i + 1, h, l1))
    return resp


def crear_pdf(nom, autor, resultat):
    file_dst = os.path.join(os.environ['USERPROFILE'], 'Downloads', f'informe_{nom}.pdf')
    c = canvas.Canvas(file_dst, pagesize=(595.27, 841.89))  # A4 pagesize
    c.setFillColor(colors.gray)
    c.rect(10, 775, 550, 20, stroke=0, fill=1)
    titul = c.beginText(50, 780)
    titul.setFont('Helvetica', 16)
    titul.setFillColor(colors.black)
    titul.textLine(f"Informe {nom}  creat per: {autor}")
    c.drawText(titul)
    c.setFont("Helvetica", 12)
    c.drawString(500, 760, f"{date.today().strftime(' %d/%m/%Y')}")
    c.drawString(50, 750, " Dades rampa original")

    image = "./static/rampa.png"
    c.drawInlineImage(image, 50, 645, width=200, height=100)
    c.line(10, 740, 555, 740)
    c.drawString(330, 710, f"L = {session['rampa_l']}  mm")
    c.drawString(330, 690, f"H = {session['rampa_h']} mm")
    c.drawString(330, 670, f"X = {session['rampa_x']} mm")

    c.drawString(50, 640, "Dades cotxe")
    cotxe = "./static/cotxe1.png"
    c.drawInlineImage(cotxe, 20, 500, width=279, height=128)
    c.line(10, 630, 555, 630)
    c.drawString(330, 610, f"B = {session['cotxe_b']} mm")
    c.drawString(330, 590, f"P = {session['cotxe_p']} mm")
    c.drawString(330, 570, f"EC = {session['cotxe_ec']} mm")
    c.drawString(330, 550, f"H = {session['cotxe_h']} mm")
    c.drawString(330, 530, f"M = {session['cotxe_m']} mm")
    c.drawString(330, 510, f"A = {session['cotxe_a']} mm")
    c.drawString(330, 490, f"Marge seguretat = {session['cotxe_ms']} mm")
    c.drawString(50, 470, "Resultats")
    resultats = "./static/solucio2.png"
    c.drawInlineImage(resultats, 20, 320, width=300, height=133)
    c.line(10, 460, 555, 460)
    punt_x_inici = 330
    punt_y_inici = 420
    for row in resultat:
        c.drawString(punt_x_inici, punt_y_inici, f"L{row[0]} = {row[2]} mm")
        c.drawString(punt_x_inici + 100, punt_y_inici, f"H{row[0]} = {row[1]} mm")
        punt_y_inici -= 20
    # finish page
    c.showPage()
    # construct and save file to .pdf
    c.save()
    return
