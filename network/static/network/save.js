function save_post(post_id) {
    
    // Get HTML contents
    let postDiv = document.getElementById(`${post_id}`);
    let postBody = postDiv.querySelector('#post-body')

    // Generate CSRF token
    let csrftoken = getCookie('csrftoken');

    // Get content to submit
    let newBody = postBody.querySelector("textarea.new-body").value.trim();

    console.log(newBody)

    // Send PUT request
    fetch(`/edit_post/${post_id}`, {
        method: "PUT",
        body: JSON.stringify({
            body: newBody,
        }),
        headers: {"X-CSRFToken": csrftoken}
    })

    .then(async(response) => {
        // If successful, update post
        if (response.status === 201) {
            
            // Show edit post and hide save post
            postDiv.querySelector('#edit-post').style.display = 'block';
            postDiv.querySelector('#save-post').style.display = 'none';
            postBody.innerHTML = `${newBody}`;
            console.log(`Post ${post_id} edited successfully`);
        }
        
        // If error, alert and reload the page
        else {
            let msg = await response.json();

            throw new Error(msg.error);                        
        }
    })

    // Catch errors
    .catch(error => {
    console.log('Error:', error);
    });
    return false;

}