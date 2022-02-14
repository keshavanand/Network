document.addEventListener('DOMContentLoaded',()=>{
    const saveButtons = document.querySelectorAll("button[name='save']");
    const editButtons = document.querySelectorAll("button[name='edit']");
    const textAreas = document.querySelectorAll("textarea[name='editContent']");
    const postContent = document.querySelectorAll("p[name='content']");
    const likeButtons = document.querySelectorAll("button[name='like']");
    saveButtons.forEach((item)=>{item.style.display = 'none';});
    textAreas.forEach((item)=>{item.style.display = 'none';});
    editButtons.forEach((item)=>{item.addEventListener('click', ()=>{

        // If user has previously clicked on edit and now he clicked on edit for other post 
        // we have to avoid editing multiple post at same time
        saveButtons.forEach((item)=>{item.style.display = 'none';});
        editButtons.forEach((item)=>{item.style.display = 'block';});
        textAreas.forEach((item)=>{item.style.display = 'none';});
        postContent.forEach((item)=>{item.style.display = 'block';});

        //Editing specific post
        const buttonNumber = item.id.substring(5);
        document.querySelector('#save-'+buttonNumber).style.display = 'block';
        document.querySelector('#edit-'+buttonNumber).style.display = 'none';
        document.querySelector('#content-'+buttonNumber).style.display = 'none';
        const postText = document.querySelector('#editContent-'+buttonNumber);
        postText.style.display = 'block';
        postText.innerHTML = document.querySelector('#content-'+buttonNumber).innerHTML;

        //Saving post
        //document.querySelector('#save-'+buttonNumber).addEventListener('click', savePost(buttonNumber));
        //saveButtons.forEach((item)=>{item.addEventListener('click', savePost(buttonNumber));});
        
    });
});
    saveButtons.forEach((item)=>{item.addEventListener('click', ()=>{
        const buttonNumber = item.id.substring(5);
        savePost(buttonNumber);
    });});

    likeButtons.forEach((item)=>{item.addEventListener('click', ()=>{
        const number = item.id.substring(5);
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const content = document.querySelector('#editContent-'+number).value;

        if (item.textContent === "Like"){
            item.textContent="Dislike";
            fetch(`/like`,{
                method: "PUT",
                headers :{'X-CSRFToken': csrftoken},
                mode: 'same-origin',
                body: JSON.stringify({
                    content: content,
                })
            }).catch((error) => console.log(error));

            
        }
        else {
            item.textContent="Like";
        }
    })});
});


function savePost(number) {
    //const number = parseInt(buttonNumber);
    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    const content = document.querySelector('#editContent-'+number).value;
    fetch(`/posts/${number}`,{
        method: "PUT",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body: JSON.stringify({
            content: content,
        })

    })// Delete below and add get to get updated post and put it on screen
    .then(()=>{
        document.querySelector('#content-'+number).innerHTML = document.querySelector('#editContent-'+number).value;
        
        document.querySelector('#save-'+number).style.display = 'none';
        document.querySelector('#edit-'+number).style.display = 'block';
        document.querySelector('#content-'+number).style.display = 'block';
        document.querySelector('#editContent-'+number).style.display='none';


    })
    .catch((error) => console.log(error));
}

