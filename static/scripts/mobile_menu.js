let menuIcon = document.getElementById('mobile-menu-icon');

menuIcon.addEventListener("click", () => {
    let menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
})