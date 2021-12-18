document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#like-icon').addEventListener('click', like_post);
});

function like_post() {
    // Save post variables
    const title = document.querySelector('#post-title').value;
   
    console.log(recipients);

    // Pass info to API
    fetch('/posts', {
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
      .then(load_likes('post'))
      
      // Catch errors
      .catch(error => {
        console.log('Error:', error);
      });
    
      return false;
}