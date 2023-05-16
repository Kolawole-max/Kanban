document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('#role_drop').forEach(item => {
        item.onclick = () => xrole(item)
    })
})

function rolll(){
    console.log("helloooo")
}

function xrole(item){

    var role_id = item.getAttribute('data-id')
    var user_id = item.getAttribute('data-user')
    console.log(user_id)

    fetch('/role', {
        method: 'PUT',
        body: JSON.stringify({
            role : role_id,
            user : user_id
        })
    })
        .then(response => response.json())
        .then(result => {
        // Print result
        console.log(result);
    });
}