let deleteButtons = document.querySelectorAll(".delete-post-btn");

deleteButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
        let targetPost = findParentWithClass(btn, "post")
        targetId = targetPost.id;
        targetPost.parentNode.removeChild(targetPost)
        sendPostRequest({ 'post_id': targetId });
    });
});

// Function to find the closest parent with a specific class
function findParentWithClass(element, className) {
    while (element && !element.classList.contains(className)) {
        element = element.parentNode;
    }
    return element;
}

function sendPostRequest(dataToSend) {
    fetch('/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
        .catch(error => {
            console.error('Error:', error);
        });
}
