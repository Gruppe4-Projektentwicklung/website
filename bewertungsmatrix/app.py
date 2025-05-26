from flask import Flask, render_template, request
import pandas as pd
import os
import json

app = Flask(__name__, static_folder='static', template_folder='templates')

def lade_ideen():
    df = pd.read_excel("daten/ideen.xlsx")
    return df

def lade_metriken():
    df = pd.read_excel("daten/metriken.xlsx")
    metriken = []
    for _, row in df.iterrows():
        metriken.append({
            "id": str(row.get("ID")),
            "titel": row.get("Kombinationstitel"),
            "formel": row.get("Formel"),
            "beschreibung": row.get("Beschreibung")
        })
    return metriken

@app.route("/")
def index():
    metriken = lade_metriken()
    return render_template("bewertung.html", metriken=metriken)

@app.route("/bewerten", methods=["POST"])
def bewerten():
    gewichtungen = request.json.get("gewichtungen")
    df_ideen = lade_ideen()
    metriken = lade_metriken()

    ergebnisse = []

    for _, idee in df_ideen.iterrows():
        score = 0
        gesamtgewicht = 0
        for metrik in metriken:
            wid = metrik["id"]
            if wid in gewichtungen:
                w = gewichtungen[wid]
                if w == 0:
                    continue
                try:
                    formel = metrik["formel"]
                    context = idee.to_dict()
                    wert = eval(formel, {}, context)
                    score += wert * w
                    gesamtgewicht += w
                except:
                    pass

        ergebnisse.append({
            "idee": idee.get("Name", "Unbenannt"),
            "score": round(score / gesamtgewicht, 2) if gesamtgewicht > 0 else 0,
            "details": idee.to_dict()
        })

    ergebnisse.sort(key=lambda x: x["score"], reverse=True)
    return json.dumps(ergebnisse)

if __name__ == "__main__":
    app.run(debug=True)
