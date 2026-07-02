fetch("http://127.0.0.1:5000/tickets")
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById("tickets");

    data.forEach(ticket => {
      const div = document.createElement("div");
      
        div.innerHTML = `
        <p><strong>Nom:</strong> ${ticket.nom}</p>
        <p><strong>Prénom:</strong> ${ticket.prenom}</p>
        <p><strong>Email:</strong> ${ticket.email}</p>
        <p><strong>Ticket:</strong> ${ticket.ticket}</p>
        <hr>
      `;
      
      
      container.appendChild(div);
    });
  })
  .catch(err => console.error(err));