console.log("admin.js chargé");

fetch("http://127.0.0.1:5000/check-admin", {
    credentials: "include"
})
.then(response => {
    if (!response.ok) {
        window.location = "/";
        throw new Error("Non connecté");
    }

    return fetch("http://127.0.0.1:5000/tickets", {
        credentials: "include"
    });
})
.then(res => res.json())
.then(data => {

     data.sort((a, b) => {
        return new Date(b.date_reservation) - new Date(a.date_reservation);
    });

    
    const compteur = document.getElementById("compteur");
    compteur.textContent = `Réservations : ${data.length}`;

    const container = document.getElementById("tickets");


    const search = document.getElementById("search");


    function afficherTickets(liste) {

        container.innerHTML = "";

        liste.forEach(ticket => {
      
      
      
          const div = document.createElement("div");
          div.classList.add("card");

          div.innerHTML = `
            <p><strong>Nom :</strong> ${ticket.nom}</p>
            <p><strong>Prénom :</strong> ${ticket.prenom}</p>
            <p><strong>Email :</strong> ${ticket.email}</p>
            <p><strong>Ticket :</strong> ${ticket.ticket}</p>
            <p><strong>Date de réservation :</strong> ${ticket.date_reservation}</p>
            <hr>
          `;

          container.appendChild(div);
    });

}

afficherTickets(data);



search.addEventListener("input", () => {

    const valeur = search.value.toLowerCase();

    const resultat = data.filter(ticket =>

        ticket.nom.toLowerCase().includes(valeur) ||
        ticket.prenom.toLowerCase().includes(valeur) ||
        ticket.email.toLowerCase().includes(valeur)
      );

      afficherTickets(resultat);

  });
})
.catch(err => console.error(err));
