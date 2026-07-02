import json
import os
import smtplib
from flask import Flask, request, jsonify
from flask_cors import CORS
from email.mime.text import MIMEText
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

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


def create_ticket_pdf(nom, prenom, ticket, dates):
    filename = f"Billet_{nom}_{prenom}.pdf"

    pdf = canvas.Canvas(filename, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(150, 800, "IBIZA PARTY 2027")

    pdf.setFont("Helvetica", 16)
    pdf.drawString(50, 740, f"Nom : {nom}")
    pdf.drawString(50, 710, f"Prénom : {prenom}")
    pdf.drawString(50, 680, f"Billet : {ticket}")

    pdf.drawString(50, 620, f"Date : {dates}")
    pdf.drawString(50, 590, "Lieu : Ibiza, Espagne")

    pdf.save()

    return filename

def send_confirmation_email(email, prenom, nom, ticket, pdf_file):
    sender = "ibizapartyelec@gmail.com"
    password = "aszd jwfd ryuc egdz"

    message = MIMEMultipart()

    message["Subject"] = "Confirmation de réservation - Ibiza Party"
    message["From"] = sender
    message["To"] = email

    body = MIMEText(
        f"""Bonjour {prenom} {nom},

Votre réservation pour Ibiza Party est confirmée !

Billet : {ticket}

Vous trouverez votre billet en pièce jointe.

Merci et à bientôt !
"""
    )

    message.attach(body)

    with open(pdf_file, "rb") as file:
        piece_jointe = MIMEApplication(file.read(), Name=pdf_file)

    piece_jointe["Content-Disposition"] = f'attachment; filename="{pdf_file}"'
    message.attach(piece_jointe)



    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        smtp.send_message(message)
    print(f"Email envoyé à {email}")









    
def get_dates(ticket):
    if ticket == "Pass 1 jour":
        return "24 juin 2027"
    elif ticket == "Pass 2 jours":
        return "24 et 25 juin 2027"
    elif ticket == "Pass jours complets":
        return "24, 25 et 26 juin 2027"
    elif ticket == "Pass VIP":
        return "24, 25 et 26 juin 2027"
    else:
        return ticket
    












@app.route("/tickets", methods=["POST"])

def create_ticket():
    data = request.get_json(silent=True)
    error = validate_ticket(data)

    if error:
        return jsonify({"error": error}), 400



    ticket_type = TICKETS[data["ticket"]]
    dates = get_dates(ticket_type)


    reservation = {
        "nom": data["nom"].strip(),
        "prenom": data["prenom"].strip(),
        "email": data["email"].strip(),
        "ticket": TICKETS[data["ticket"]],
        "dates": dates

    
    
    
    }

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            reservations = json.load(file)
    else:
        reservations = []

    reservations.append(reservation)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(reservations, file, indent=4, ensure_ascii=False)
    
    
    pdf_file = create_ticket_pdf(
    reservation["nom"],
    reservation["prenom"],
    reservation["ticket"],
    reservation["dates"]
)
    
    
    
    try:
        send_confirmation_email(
            reservation["email"],
            reservation["prenom"],
            reservation["nom"],
            reservation["ticket"],
            pdf_file
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



