async function loadItems() {
    let response = await fetch('/people');
    let items = await response.json();
    //console.log(items);
    let itemsContainer = document.getElementById('peopleTable');
    itemsContainer.innerHTML = '';
    items.forEach(item => {
        let row = document.createElement('tr');
        row.setAttribute("data-id", item.person_id);
        row.innerHTML = `<td>${item.first_name}</td><td>${item.last_name}</td>`;
        itemsContainer.appendChild(row);
    });

    addEventListeners()
}

async function addEventListeners() {
    document.querySelectorAll("#peopleTable tr").forEach(row => {
        row.addEventListener("click", async function () {
            let personId = this.getAttribute("data-id");
            let first = this.cells[0].innerText;
            let last = this.cells[1].innerText;
            response = await fetch(`/emails/${personId}`)
                .then(response => response.json())
                .then(data => {
                    console.log(data)

                    // Successful request: Update the righthand-side form elements
                    let firstNameFormInp = document.getElementById("first_name");
                    firstNameFormInp.value = first;
                    let lastNameFormInp = document.getElementById("last_name");
                    lastNameFormInp.value = last;

                    let emailDetailDiv = document.getElementById("email-list");
                    data.forEach(dbItem => {
                        emailDetailDiv.innerHTML = `<p>Email: ${dbItem.email}</p>`;
                    });
                })
                .catch(error => console.error("Error fetching person details:", error));
        });
    });
}

// Alright now do stuff
window.onload = loadItems;