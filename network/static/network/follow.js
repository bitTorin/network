function follow(profile) {
  
  // Assign parent div to variable
  let followDiv = document.querySelector("#follow-status");
      
  // Generate CSRF token
  let csrftoken = getCookie('csrftoken');

  // Send POST request
  fetch(`/follow`, {
    method: "POST",
    body: JSON.stringify({
      profile: profile,
        
    }),
    headers: {"X-CSRFToken": csrftoken}
  })

  .then(async(response) => {
      // If successful, update post
      if (response.status === 201) {
          
          // Hide empty icon and show filled icon
          followDiv.querySelector('#follow').style.display = 'none';
          followDiv.querySelector('#unfollow').style.display = 'inline-block';

          // Success message
          console.log(`User ${profile} followed successfully`);
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

function unfollow(profile) {

  // Assign parent div to variable
  let followDiv = document.querySelector("#follow-status");
    
  // Generate CSRF token
  let csrftoken = getCookie('csrftoken');

  // Send POST request
  fetch(`/unfollow`, {
    method: "POST",
    body: JSON.stringify({
      profile: profile,
        
    }),
    headers: {"X-CSRFToken": csrftoken}
  })

  .then(async(response) => {
      // If successful, update post
      if (response.status === 201) {
          
          // Hide empty icon and show filled icon
          followDiv.querySelector('#follow').style.display = 'inline-block';
          followDiv.querySelector('#unfollow').style.display = 'none';

          // Success message
          console.log(`User ${profile} unfollowed successfully`);
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