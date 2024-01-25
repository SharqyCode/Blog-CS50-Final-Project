let addDesc = document.getElementById("add_description");
let btnCancel = document.getElementById("btn_cancel");
let editDesc = document.getElementById("edit_description");
let descScreen = document.getElementById("desc_screen");
// let btnSave = document.querySelector("#btn_save");
// let description = document.querySelector("#description");

let counter = document.getElementById('counter');
let maxCharacters = parseInt(editDesc.getAttribute('maxlength'));

addDesc.addEventListener("click", () => {
    descScreen.classList.remove("hidden");
    document.body.style.overflow = 'hidden';
    editDesc.selectionStart = editDesc.value.length;
    editDesc.focus();
})
btnCancel.addEventListener("click", (e) => {
    e.preventDefault();
    descScreen.classList.add("hidden");
    document.body.style.overflow = 'scroll'
})

// Initial setup of the counter
updateCounter();

// Add an input event listener to the editDesc
editDesc.addEventListener('input', function () {
    updateCounter();
});

function updateCounter() {
    let currentCharacters = editDesc.value.length;
    let remainingCharacters = maxCharacters - currentCharacters;

    // Update the counter text
    counter.textContent = "Max Characters: " + remainingCharacters;

    // Optionally, you can style the counter based on the remaining characters
    if (remainingCharacters <= 0) {
        counter.style.color = 'rgb(239 68 68)'; // Change to a color indicating over the limit
    } else {
        counter.style.color = 'unset'; // Change to the default color
    }
}