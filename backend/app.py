from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"
REQUIRED_FIELDS = ["nom", "prenom", "email", "ticket"]
TICKETS = {
    "1jour": "Pass 1 jour",
    "2jours": "Pass 2 jours",
    "3jours": "Pass jours complets",
    "vip": "Pass VIP"
} 


def validate_ticket(data):
    if not data:
        return "Les données de réservation sont obligatoires."

    for field in REQUIRED_FIELDS:
        if field not in data or not str(data[field]).strip():
            return f"Le champ '{field}' est obligatoire."

    if "@" not in data["email"] or "." not in data["email"]:
        return "L'adresse email n'est pas valide."

    if data["ticket"] not in TICKETS:
        return "Le type de billet n'est pas valide."

    return None

def send_confirmation_email(email, prenom, nom, ticket):
    sender = "ibizapartyelec@gmail.com"
    password = "aszd jwfd ryuc egdz"

    message = MIMEText(
        f"""Bonjour {prenom} {nom},

Votre réservation pour Ibiza Party est confirmée !

Billet : {ticket}

Merci et à bientôt !
"""
    )

    message["Subject"] = "Confirmation de réservation - Ibiza Party"
    message["From"] = sender
    message["To"] = email

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        smtp.send_message(message)
    print(f"Email envoyé à {email}")

@app.route("/tickets", methods=["POST"])

def create_ticket():
    data = request.get_json(silent=True)
    error = validate_ticket(data)

    if error:
        return jsonify({"error": error}), 400

    reservation = {
        "nom": data["nom"].strip(),
        "prenom": data["prenom"].strip(),
        "email": data["email"].strip(),
        "ticket": TICKETS[data["ticket"]]
    }

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            reservations = json.load(file)
    else:
        reservations = []

    reservations.append(reservation)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(reservations, file, indent=4, ensure_ascii=False)
    
    try:
        send_confirmation_email(
            reservation["email"],
            reservation["prenom"],
            reservation["nom"],
            reservation["ticket"]
        )
    except Exception as e:
        print("Erreur email :", e)
    return jsonify({"message": "Réservation enregistrée"}), 201


@app.route("/tickets", methods=["GET"])
def get_tickets():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            reservations = json.load(file)
    else:
        reservations = []

    return jsonify(reservations)


if __name__ == "__main__":
    app.run(debug=True)
