var socket = io.connect(window.location.protocol+'//'+document.domain+':'+location.port+'/getimages');

let main_add =  document.getElementById('head');

document.addEventListener('keydown',function(event){
    if(event.keyCode == 13)
    {
        search();
    }
})

window.onbeforeunload=function(e){
    socket.disconnect();
}


function search()
{
    event.preventDefault();
    let query = document.forms[0].elements[0].value;
    let s_query = {};
    s_query['query'] = query;
    socket.emit('query',s_query);
    console.log('send query');
}

//on receive query by the server then
socket.on('query_recv',function(message){
    console.log(message);
    document.getElementById('load_more').disabled = false;
    document.getElementById('load_more').innerHTML = "LOAD MORE";
});

function getlink()
{
    if(document.getElementById('load_more').disabled==false)
    {
        let howmany = {};
        let images_to_laod;
        if(document.getElementById('howmany').value == '')
            images_to_laod = 3
        else
            images_to_laod = parseInt(document.getElementById('howmany').value);

        howmany['images'] = images_to_laod;
        socket.emit('getlink',howmany);
    }
}

function create_div(link)
{
    //console.log(link," ",link.length);
    //for(let i=0;i<link.length;i++)
    //{
        let image_div = document.createElement('div');
        image_div.classList.add('image');
        let img =document.createElement('img');
        //img.src = link[i]['link'];
        img.src = link['link'];

        image_div.appendChild(img);
        document.getElementById('img-cont').appendChild(image_div);

        let infodiv = document.createElement('div') ;
        infodiv.classList.add('info');

        let p = document.createElement('p');
        //p.innerHTML = "Size : " + link[i]['width'] + " x " + link[i]['height'];
        p.innerHTML = "Size : " + link['width'] + " x " + link['height'];
        
        let a =document.createElement('a');
        //a.href = link[i]['link'];
        a.href = 'data:image/jpg;base64,' + link['data'];
        a.target ='_blank';
        a.setAttribute('download',link['image_name']);
        a.innerHTML = document.getElementById('download').innerHTML;
        
        infodiv.appendChild(p);
        infodiv.appendChild(a);

        image_div.appendChild(infodiv);
        //window.scrollTo(0,document.body.scrollHeight);
    //}

}
socket.on('getimage',function(link){
    create_div(link);
    //console.log(link);
});

socket.on('onconnect',function(message){
    console.log(message)
});
