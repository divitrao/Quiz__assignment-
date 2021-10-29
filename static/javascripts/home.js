if(document.getElementById('logout_id')!=null){
    document.getElementById('logout_id').onclick = ()=>{
        console.log('clicked')
        const requestOptions_logout = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify()
        };
    
        fetch('http://127.0.0.1:8000/logout/',requestOptions_logout)
        .then(
            location.reload()
        )
    
    }
}

