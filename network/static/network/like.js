function like_post(post_id) {

  // Get HTML contents
  let PostDiv = document.getElementById(`${post_id}`);

  let likeDiv = PostDiv.querySelector("#likes");

  let likeCount = likeDiv.querySelector('#likeCount');
  let likes = parseInt(likeCount.getAttribute('value'), 10);

  // Generate CSRF token
  let csrftoken = getCookie('csrftoken');

  // Send POST request
  fetch(`/like_post`, {
    method: "POST",
    body: JSON.stringify({
      post_id: post_id,
        
    }),
    headers: {"X-CSRFToken": csrftoken}
  })

  .then(async(response) => {
      // If successful, update post
      if (response.status === 201) {
          
          // Hide empty icon and show filled icon
          likeDiv.querySelector('#icon-filled').style.display = 'inline-block';
          likeDiv.querySelector('#icon-empty').style.display = 'none';
          
          // Update like count
          likeCount.innerHTML = likes + 1;

          // Success message
          console.log(`Post ${post_id} liked successfully`);
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

function unlike_post(post_id) {

  // Get HTML contents
  let PostDiv = document.getElementById(`${post_id}`);

  let likeDiv = PostDiv.querySelector("#likes");

  let likeCount = likeDiv.querySelector('#likeCount');
  let likes = parseInt(likeCount.getAttribute('value'), 10);

  // Generate CSRF token
  let csrftoken = getCookie('csrftoken');

  // Send POST request
  fetch(`/unlike_post`, {
    method: "POST",
    body: JSON.stringify({
      post_id: post_id,
        
    }),
    headers: {"X-CSRFToken": csrftoken}
  })

  .then(async(response) => {
      // If successful, update post
      if (response.status === 201) {
          
          // Hide empty icon and show filled icon
          likeDiv.querySelector('#icon-filled').style.display = 'none';
          likeDiv.querySelector('#icon-empty').style.display = 'inline-block';

          // Update like count
          likeCount.innerHTML = likes - 1;

          // Success message
          console.log(`Post ${post_id} unliked successfully`);
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