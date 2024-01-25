let editCover = document.querySelector("#edit_cover_label") // label
let uploadCover = document.querySelector("#upload_cover") // input
let submitCover = document.querySelector("#submit_cover") // button

let editPfp = document.querySelector("#edit_pfp_label") // label
let uploadPfp = document.querySelector("#upload_pfp") // input
let submitPfp = document.querySelector("#submit_pfp") // button

editCover.addEventListener("click", () => {
    uploadCover.addEventListener("change", () => {
        submitCover.style.display = "inline";
    });
});

editPfp.addEventListener("click", () => {
    uploadPfp.addEventListener("change", () => {
        submitPfp.style.display = "flex";
    });
});
