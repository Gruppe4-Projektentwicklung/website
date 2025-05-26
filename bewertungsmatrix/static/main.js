document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("metriken-container");
  const ergebnisListe = document.getElementById("ergebnis-liste");

  metriken.forEach((metrik) => {
    const wrapper = document.createElement("div");
    wrapper.classList.add("metrik-eintrag");

    const label = document.createElement("label");
    label.innerHTML = `
      <strong>${metrik.titel}</strong>
      <span class="info" title="${metrik.beschreibung}">[?]</span>
    `;

    const select = document.createElement("select");
    select.name = metrik.id;
    for (let i = 0; i <= 5; i++) {
      const option = document.createElement("option");
      option.value = i;
      option.textContent = i;
      select.appendChild(option);
    }

    wrapper.appendChild(label);
    wrapper.appendChild(select);
    container.appendChild(wrapper);
  });

  document.getElementById("bewertungs-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const selects = document.querySelectorAll("select");
    const gewichtungen = {};
    selects.forEach((sel) => {
      gewichtungen[sel.name] = parseInt(sel.value);
    });

    const res = await fetch("/bewerten", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ gewichtungen }),
    });
    const daten = await res.json();

    ergebnisListe.innerHTML = "";
    daten.forEach((eintrag) => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${eintrag.idee}</strong> – Score: ${eintrag.score}`;
      ergebnisListe.appendChild(li);
    });
  });
});