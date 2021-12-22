function edit_post(post_id) {

    console.log(post_id)

    // Get HTML contents
    let postDiv = document.getElementById(`${post_id}`);

    // Show save post and hide edit post
    postDiv.querySelector('#edit-post').style.display = 'none';
    postDiv.querySelector('#save-post').style.display = 'block';

    let postBody = postDiv.querySelector('#post-body')
    
    let bodyText = postBody.getAttribute('value')
    console.log(bodyText)

    postBody.innerHTML = `<textarea class="form-control new-body" id="post_body" value="${bodyText}">${bodyText}</textarea>`

}