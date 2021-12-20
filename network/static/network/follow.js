document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#follow').addEventListener('click', follow);
    document.querySelector('#unfollow').addEventListener('click', unfollow);
});

function follow() {

      // Show the mailbox and hide other views
    document.querySelector('#follow').style.display = 'block';
    document.querySelector('#unfollow').style.display = 'none';
    
    // Pass info to API
    fetch('/profile', {
        method: 'POST',
        body: JSON.stringify({
            // TODO
        })
      })
      .then(response => response.json())
      
      .then(result => {
        // Print result
        console.log(result);
      })
    
      // Re-load likes TODO - FUNCTION NEEDED
      .then(load_follow('post'))
      
      // Catch errors
      .catch(error => {
        console.log('Error:', error);
      });
    
      return false;
}

function unfollow() {
    
  // Pass info to API
  fetch('/profile', {
      method: 'POST',
      body: JSON.stringify({
          // TODO
      })
    })
    .then(response => response.json())
    
    .then(result => {
      // Print result
      console.log(result);
    })
  
    // Re-load likes TODO - FUNCTION NEEDED
    .then(load_follow('post'))
    
    // Catch errors
    .catch(error => {
      console.log('Error:', error);
    });
  
    return false;
}