let form = document.querySelector('.messageForm');



let data = [];

function getMsg(){
    fetch('/api/message', {
        method:'GET'
    }).then(response => response.json())
    .then(result => {
        console.log(result)
        data = result;
        renderMsg();
    })
    
}

function postMsg(){
    let formData = new FormData();
    
    let text = document.querySelector('.formText').value;
    let file = document.querySelector('input[type="file"]')
    file = file.files[0]
    // console.log(input.files[0])
    formData.append('text', text);
    formData.append('file', file);
    
    fetch('/api/message', {
        method:'POST',
        body:formData 
    }).then(response => response)
    .then(result => {
        console.log(result);
        getMsg();
    })
}

// https://aru0828practicebucket.s3.ap-northeast-2.amazonaws.com/20210611.jpg

function renderMsg(){
    
    let container = document.querySelector('.container');
   
    container.innerHTML = "";
    data.data.forEach(item => {

        let div = document.createElement('div');
        let p = document.createElement('p');
        let img = document.createElement('img');

        p.textContent = item.message_text;
        img.setAttribute('src', item.message_img_url.replace('aru0828practicebucket.s3.ap-northeast-2.amazonaws.com','dms6s4gb7j5zs.cloudfront.net'));

        div.appendChild(p);
        div.appendChild(img);
        container.appendChild(div);
    })
    document.querySelector('body').appendChild(container);
}

form.addEventListener('submit', function(e){
    e.preventDefault();
    postMsg();
})


getMsg();