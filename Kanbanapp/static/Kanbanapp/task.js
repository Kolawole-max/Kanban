var comment_box
var type
var send_button
var edit_button
var comment_id
document.addEventListener('DOMContentLoaded', () => {

    const role = JSON.parse(document.getElementById('role').textContent);
    const user = JSON.parse(document.getElementById('user').textContent);
    task_id = JSON.parse(document.getElementById('task_id').textContent);

    comment_box = document.querySelector('#comment_box')

    if(role != 'Customers'){

        comment_box = document.querySelector('#comment_box')

        send_button = document.querySelector('#send_button');
        edit_button = document.querySelector('#edit_button')

        send_button.addEventListener('click', () => send_comment(task_id));
        edit_button.addEventListener('click', () => edit(task_id));
        
        if(document.querySelector('#plus') != null){
            document.querySelector('#plus').addEventListener('click', ()=> pluss(task_id))
        }

        document.querySelectorAll('#editbutton').forEach(item => {
            item.onclick = () => edit_comment(item)
        })
        document.querySelectorAll('#delete_button').forEach(item => {
            item.onclick = () => delete_(task_id, item)
        })
        
    }
})


function send_comment(task_id) {

    var content = comment_box.value
    if(content != ""){
        fetch('/comment/' + task_id , {
            method: 'POST',
            body: JSON.stringify({
                description : content
            })
        })
            .then(response => response.json())
            .then(result => {
            // Print result
            console.log(result);
            comment_box.value = ""
        });
    }
    
}

function edit_comment(item) {
    
    edit_button.style.visibility = 'visible';
    send_button.style.visibility = 'hidden';

    var content_desc = item.getAttribute('data-des') 
    comment_id = item.getAttribute('data-id')

    comment_box.value = content_desc
    var div =  document.querySelector('#div' + comment_id)
    div.remove()

}

function edit(task_id) {

    var content = comment_box.value

    fetch('/comment/' + task_id , {
        method: 'PUT',
        body: JSON.stringify({
            comment_id : comment_id,
            description : content
        })
    })
        .then(response => response.json())
        .then(result => {
          // Print result
            console.log(result);
            edit_button.style.visibility = 'hidden';
            send_button.style.visibility = 'visible';
            comment_box.value = ""
    });
}

function delete_(task_id, item){
    var comment_id = item.getAttribute('data-id')
    fetch('/comment/' + task_id , {
        method: 'DELETE',
        body: JSON.stringify({
            comment_id : comment_id,
            type : 'delete'
        })
    })
        .then(response => response.json())
        .then(result => {
          // Print result
          console.log(result);
          const div = document.querySelector('#div' + comment_id)
          div.style.display = "none"
    });
}

function pluss(task_id) {

    const estimate_left = JSON.parse(document.getElementById('estimate_left').textContent);
    const progress_hours = JSON.parse(document.getElementById('progress_hours').textContent);

    var new_progress = document.querySelector('#plusandminustext').value
    
    fetch('/hour', {
        method: 'PUT',
        body: JSON.stringify({
            new_progress : new_progress,
            task_id : task_id
        })
    })
        .then(response => response.json())
        .then(result => {
        // Print result
        console.log(result);

        document.querySelector('#plusandminustext').value = 0
        var esti = estimate_left - new_progress
        document.querySelector('#estimated').innerHTML = "Estimated time left: " + esti + " hour(s)"
    

        if(estimate_left == new_progress){
                
            document.querySelector('#status').innerHTML = "Task status: Completed"
            var plusdiv = document.querySelector('#plusdiv')
            plusdiv.style.display = "none"

            fetch('/status/' + task_id , {
                method: 'PUT',
                body: JSON.stringify({
                    status : 3
                })
            })
                .then(response => response.json())
                .then(result => {
                // Print result
                console.log(result);
            });
        }
    });
}
