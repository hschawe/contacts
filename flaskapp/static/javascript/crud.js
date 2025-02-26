let num_emails = 0;

function resetForm() {
    document.getElementById("main-form").innerHTML = `
        <input style="display:none;" id="person_id" type="text" value=""/>

        <div id="name-input-container">
            <div style="float:left;margin-right:20px;">
                <label class="name-input-label" for="first_name">First Name</label>
                <input class="name-form-text-input" id="first_name" type="text" />
            </div>

            <div style="float:left;margin-right:20px;">
                <label class="name-input-label" for="last_name">Last Name</label>
                <input class="name-form-text-input" id="last_name" type="text" />
            </div>
        </div>
        <div id="email-list-main-container">
            <label class="name-input-label">Email</label>
            <div id="email-list"></div>
            <div id="email-list-add-button-container">
                <span class="material-symbols-outlined md-24 my-blue">add_circle</span>
                <span id="add-email-text" class="my-blue">add email</span>
            </div>
        </div>`
}

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
                    // Successful request: Update the righthand-side form elements
                    let firstNameFormInp = document.getElementById("first_name");
                    firstNameFormInp.value = first;
                    let lastNameFormInp = document.getElementById("last_name");
                    lastNameFormInp.value = last;

                    let emailDetailDiv = document.getElementById("email-list");
                    for (let i=0; i<data.length; i++) {
                        emailDetailDiv.innerHTML = `<input type="text" class="emailTextInput" name="inputs[]" value="${data[i].email}" readonly>`;
                    }
                })
                .catch(error => console.error("Error fetching person details:", error));
        });
    });
}

async function addEmail() {
    // Add an editable email to the form
    let emailDetailDiv = document.getElementById("email-list");
    let newInputContainer = document.createElement('div');
    newInputContainer.setAttribute("class", "email-form-input-container")
    newInputContainer.innerHTML = `<input type="text" class="email-text-input" name="inputs[]" placeholder="type here..."><button type="button" class="email-text-input-delete-button" onclick="removeEmail(this)"><span class="material-symbols-outlined md-24 my-red">do_not_disturb_on</span></button>`;
    emailDetailDiv.appendChild(newInputContainer);
}

async function removeEmail(e) {
    // Remove email from the form
    console.log(e)
}

// Alright now do stuff
window.onload = loadItems;