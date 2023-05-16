
document.addEventListener('DOMContentLoaded', () => {

    const username = JSON.parse(document.getElementById('username').textContent);
    
    if(username == 'Customers'){

        document.querySelectorAll('#priority').forEach(item => {
            item.onclick = () => priorityy(item)
        })
    } else {

        document.querySelectorAll('#status').forEach(item => {
            item.onclick = () => statuss(item)
        })
    }
    
})

function priorityy(item){
    
    var task_id = item.getAttribute('data-task')
    var id = item.getAttribute('data-id')
    console.log(id)

    fetch('/priority/' + task_id , {
        method: 'PUT',
        body: JSON.stringify({
            priority : id
        })
    })
        .then(response => response.json())
        .then(result => {
        // Print result
        console.log(result);
    });
}

function statuss(item){
    var status_id = item.getAttribute('data-status')
    var task_id = item.getAttribute('data-id')
    console.log(task_id)
    fetch('/status/' + task_id , {
        method: 'PUT',
        body: JSON.stringify({
            status : status_id
        })
    })
        .then(response => response.json())
        .then(result => {
        // Print result
        console.log(result);
    });
}