document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#edit-post').addEventListener('click', edit_post);
});

function edit_post(post_id) {

    

    // Load post
    fetch(`/edit_post/${post_id}`)
    .then(response => response.json())
    .then(post => {

        // Print emails
        console.log(post);

        // Assign variable
        const body = post.body;

        


    })
}