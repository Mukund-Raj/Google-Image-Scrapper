
var socket = io.connect('http://'+document.domain+':'+location.port+'/getimage');

let main_add =  document.getElementById('head');

function clickme(button) {
    console.log(button);
}

function search()
{
    event.preventDefault();

    let query = document.forms[0].elements[0].value;
    let formdata = new FormData();
    formdata.append('query',query);

    let xhr = new XMLHttpRequest();
    xhr.open('POST','/query',true);
    xhr.send(formdata);
    xhr.onload = function(){
    if(xhr.readyState == 4 && xhr.status == 200)
    {
        console.log(xhr.response);
    }
    else
    {
        console.log("error occured");
    }
    } 

}

function getlink()
{
    /*
    let xhr = new XMLHttpRequest();
    xhr.responseType = 'json';

    xhr.open('GET','/getlink',true);
    xhr.send();

    xhr.onload = function(){
    if(xhr.readyState == 4 && xhr.status == 200)
    {
        console.log(xhr.response);
        let link_we_get = xhr.response;
        create_div(link_we_get["all_links"])
    }
    else
    {
        console.log("error occured");
    }
    }
*/
let howmany = {}
howmany['images'] = 50;
socket.emit('getlink',howmany);

}

function create_div(link)
{
    console.log(link," ",link.length);
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
        window.scrollTo(0,document.body.scrollHeight);
    //}

}
socket.on('getimage',function(link){
    create_div(link);
    console.log(link);
});
