// document.addEventListener('DOMContentLoaded', function() {
//     document.querySelector('#empty-like-icon').addEventListener('click', like_post);
// });

function like_post(post_id, user) {

  console.log(post_id)
  console.log(user)

  // Concert username to string
  username = user.toString()

  // Get HTML contents
  let PostDiv = document.getElementById(`${post_id}`);

  let likeDiv = PostDiv.querySelector("#likes");

  // // Show empty icon and hide filled icon
  // likeDiv.querySelector('#icon-filled').style.display = 'none';
  // likeDiv.querySelector('#icon-empty').style.display = 'inline-block';

  let likeCount = likeDiv.querySelector('#likeCount');
  let likes = parseInt(likeCount.getAttribute('value'), 10);
  
  console.log(likes)

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

function unlike_post(post_id, user) {

  console.log(post_id)
  console.log(user)

  // Concert username to string
  // username = user.toString()

  // Get HTML contents
  let PostDiv = document.getElementById(`${post_id}`);

  let likeDiv = PostDiv.querySelector("#likes");

  // // Show empty icon and hide filled icon
  // likeDiv.querySelector('#icon-filled').style.display = 'inline-block';
  // likeDiv.querySelector('#icon-empty').style.display = 'none';

  let likeCount = likeDiv.querySelector('#likeCount');
  let likes = parseInt(likeCount.getAttribute('value'), 10);
  
  console.log(likes)

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