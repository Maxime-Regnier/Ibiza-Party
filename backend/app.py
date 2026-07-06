import json
import os
import smtplib
from flask_cors import CORS
from email.mime.text import MIMEText
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from flask import Flask, send_from_directory, request, jsonify, session
from datetime import datetime
from reportlab.lib.utils import ImageReader



app = Flask(__name__, static_folder="../frontend")
app.secret_key = "huber58:grrignaud"


CORS(app, supports_credentials=True)


DATA_FILE = "data.json"
REQUIRED_FIELDS = ["nom", "prenom", "email", "ticket"]

ADMIN_PASSWORD = "Ibiza2027"

TICKETS = {
    "1jour": "Pass 1 jour",
    "2jours": "Pass 2 jours",
    "3jours": "Pass 3 jours",
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
    logo = ImageReader("logo.webp")
    pdf.drawImage(logo, 240, 700, width=120, height=120, mask='auto')
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
    if ticket == "1jour":
        return "24 juin 2027"
    elif ticket == "2jours":
        return "24 et 25 juin 2027"
    elif ticket == "3jours":
        return "24, 25 et 26 juin 2027"
    elif ticket == "vip":
        return "24, 25 et 26 juin 2027"
    else:
        return ticket
    



@app.route("/")
def home():
    return send_from_directory("../frontend", "login.html")


@app.route("/admin")
def admin_page():
    return send_from_directory("../frontend", "admin.html")

@app.route("/admin.css")
def admin_css():
    return send_from_directory("../frontend", "admin.css")


@app.route("/admin.js")
def admin_js():
    return send_from_directory("../frontend", "admin.js")


@app.route("/style.css")
def style_css():
    return send_from_directory("../frontend", "style.css")


@app.route("/script.js")
def script_js():
    return send_from_directory("../frontend", "script.js")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "password" not in data:
        return jsonify({"error": "Mot de passe manquant"}), 400
    if data["password"] == ADMIN_PASSWORD:
        session["admin"] = True
        return jsonify({"success": True}), 200

    return jsonify({"error": "Mot de passe incorrect"}), 401


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("admin", None)
    return jsonify({"success": True})


@app.route("/check-admin", methods=["GET"])
def check_admin():
    if session.get("admin"):
        return jsonify({"connected": True})

    return jsonify({"connected": False}), 401


@app.route("/tickets", methods=["POST"])
def create_ticket():
    data = request.get_json(silent=True)
    error = validate_ticket(data)

    if error:
        return jsonify({"error": error}), 400

    ticket_type = TICKETS[data["ticket"]]
    dates = get_dates(data["ticket"])


    reservation = {
        "nom": data["nom"].strip(),
        "prenom": data["prenom"].strip(),
        "email": data["email"].strip(),
        "ticket": TICKETS[data["ticket"]],
        "dates": dates,
        "date_reservation": datetime.now().strftime("%d/%m/%Y à %H:%M")


    
    
    
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
    
    if not session.get("admin"):
        return jsonify({"error": "Accès interdit"}), 401
    
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            reservations = json.load(file)
    else:
        reservations = []

    return jsonify(list(reversed(reservations)))




@app.route("/image/<path:filename>")
def images(filename):
    return send_from_directory("../frontend/image", filename)




if __name__ == "__main__":
    app.run(debug=True)
