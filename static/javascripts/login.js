// const csrfToken = getCookie('csrftoken');
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
// const headers = new Headers({
//         'Content-Type': 'x-www-form-urlencoded',
//         'X-CSRF-TOKEN': csrfToken
//     });

    document.getElementById('login_submit').onclick = ()=>{
        // console.log('clikced')
        // console.log(getCookie('csrftoken'))
        // console.log(document.getElementById('username').value)
        // console.log(document.getElementById('password').value)
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: document.getElementById('username').value
                                ,password:document.getElementById('password').value })
        };

        

        fetch('http://127.0.0.1:8000/login/', requestOptions)
        .then(
            response => {
                if(response.ok==true){
                    location.href = 'http://127.0.0.1:8000/'
                }
                
            })
        
    }

    
   


   