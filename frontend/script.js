const eventDate = new Date("2027-06-24T17:00:00");

function updateCountdown() {
    const now = new Date();
    const diff = eventDate - now;

    if (diff <= 0) return;

    document.getElementById("days").textContent =
        Math.floor(diff / (1000 * 60 * 60 * 24));

    document.getElementById("hours").textContent =
        Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));

    document.getElementById("minutes").textContent =
        Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

    document.getElementById("seconds").textContent =
        Math.floor((diff % (1000 * 60)) / 1000);
}

setInterval(updateCountdown, 1000);
updateCountdown();

function showReservationSuccess() {

    const form = document.getElementById("ticket-form");
    const confirmation = document.getElementById("confirmation-message");

    console.log(form);
    console.log(confirmation);

    form.style.display = "none";
    confirmation.classList.add("show");
}

const form = document.getElementById("ticket-form");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const submitButton = form.querySelector("button[type='submit']");

    submitButton.disabled = true;
    submitButton.textContent = "Envoi en cours...";

    const data = {
        nom: document.getElementById("nom").value,
        prenom: document.getElementById("prenom").value,
        email: document.getElementById("email").value,
        ticket: document.getElementById("ticket").value
    };

    console.log("Données envoyées :", data);

    try {
        const response = await fetch("http://127.0.0.1:5000/tickets", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        console.log("Status :", response.status);

        const result = await response.text();

        console.log("Réponse backend :", result);

        if (!response.ok) {
            throw new Error(result);
        }

        console.log("Avant showReservationSuccess");
showReservationSuccess();
console.log("Après showReservationSuccess");

    } catch (error) {
        console.error("Erreur :", error);

        alert("Impossible d'enregistrer la réservation.");

        submitButton.disabled = false;
        submitButton.textContent = "Valider ma réservation";
    }
});

document.getElementById("date").textContent = new Date().getFullYear();

const buttons = document.querySelectorAll(".tab-btn");
const contents = document.querySelectorAll(".tab-content");

buttons.forEach(btn => {
    btn.addEventListener("click", () => {
        const target = btn.dataset.day;

        buttons.forEach(b => b.classList.remove("active"));
        contents.forEach(c => c.classList.remove("active"));

        btn.classList.add("active");
        document.getElementById(target).classList.add("active");
    });
});