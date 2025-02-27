function resetForm() {
    document.getElementById("top-form-container").innerHTML = `
        <div id="name-input-container">
            <div style="float:left;margin-right:20px;">
                <label class="name-input-label" for="first_name">First Name</label>
                <input class="name-form-text-input" id="first_name" name="first_name" type="text" />
            </div>

            <div style="float:left;margin-right:20px;">
                <label class="name-input-label" for="last_name">Last Name</label>
                <input class="name-form-text-input" id="last_name" name="last_name" type="text" />
            </div>
        </div>
        <div id="email-list-main-container">
            <label class="name-input-label">Email</label>
            <div id="email-list"></div>
            <div id="email-list-add-button-container" onclick="addEmail()">
                <span class="material-symbols-outlined md-24 my-blue">add_circle</span>
                <span id="add-email-text" class="my-blue">add email</span>
            </div>
        </div>`

       document.getElementById("person_id").value = "";
}

async function loadItems() {
    let response = await fetch('/people');
    let items = await response.json();
    //console.log(items);
    let itemsContainer = document.getElementById('people-name-list');
    itemsContainer.innerHTML = '';
    items.forEach(item => {
        let row = document.createElement('li');
        row.setAttribute("data-id", item.person_id);
        row.setAttribute("data-fname", item.first_name);
        row.setAttribute("data-lname", item.last_name);
        row.innerHTML = `${item.first_name} ${item.last_name}`;
        itemsContainer.appendChild(row);
    });

    addEventListeners()
}

async function addEventListeners() {
    // Add name listeners
    document.querySelectorAll("#people-name-list li").forEach(row => {
        row.addEventListener("click", async function () {
            let personId = this.getAttribute("data-id");
            let first = this.getAttribute("data-fname");
            let last = this.getAttribute("data-lname");
            response = await fetch(`/emails/${personId}`)
                .then(response => response.json())
                .then(data => {
                    // Successful request: Update the righthand-side form elements
                    document.getElementById("person_id").value = personId;
                    document.getElementById("first_name").value = first;
                    document.getElementById("last_name").value = last;

                    let emailDetailDiv = document.getElementById("email-list");
                    emailDetailDiv.innerHTML = "";
                    for (let i=0; i<data.length; i++) {
                        let newEmailInput = document.createElement('div')
                        newEmailInput.setAttribute("class", "email-form-input-container")
                        newEmailInput.innerHTML = `
                        <input type="text" class="email-text-input" name="inputs[]" value="${data[i].email}" readonly>
                        <button type="button" class="email-text-input-delete-button" onclick="removeEmail(this);">
                        <span class="material-symbols-outlined md-24 my-red">do_not_disturb_on</span>
                        </button>`;

                        emailDetailDiv.appendChild(newEmailInput);
                    }
                })
                .catch(error => console.error("Error fetching person details:", error));
        });
    });

    // Remove default form behavior
    const form = document.getElementById('main-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
    })
}

async function addEmail() {
    // Add an editable email to the form
    let emailDetailDiv = document.getElementById("email-list");
    let newInputContainer = document.createElement('div');
    newInputContainer.setAttribute("class", "email-form-input-container")
    newInputContainer.innerHTML = `<input type="text" class="
    email-text-input" name="inputs[]" placeholder="type here..."><button type="button" class="email-text-input-delete-button" onclick="removeEmail(this);"><span class="material-symbols-outlined md-24 my-red">do_not_disturb_on</span></button>`;
    emailDetailDiv.appendChild(newInputContainer);
}

async function removeEmail(btn) {
    // Remove the email container from the form
    btn.parentNode.parentNode.removeChild(btn.parentNode);
}

async function submitSave() {
    const form = document.getElementById('main-form');
    const formData = new FormData(form);
    try {
        const response = await fetch('/', {
            method: 'POST',
            body: formData
        });
        if (!response.ok) {
            console.error('Error submitting form.');
        }
    } catch (error) {
        console.error('There was an error:', error);
    }

    // Reset the form elements & refresh the contact names sidebar
    resetForm();
    loadItems();
}

async function submitDelete() {
    const person_id = document.getElementById('person_id').value;

    const response = await fetch('/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"person_id": person_id})
    });
    if (!response.ok) {
        console.error('DELETE failed');
    }

    // Reset the form elements & refresh the contact names sidebar
    resetForm();
    loadItems();
}

window.onload = loadItems;