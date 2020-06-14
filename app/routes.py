from app import flask_app,socketio
from flask import render_template,request,jsonify,session
from app.gimage import start_scrapper,get_image_link,search_query,total_images
from app.Image_File_Name import Image_Name
import base64
import requests
from .User import User
from app import all_users
#get image link generator global object 
next_link = None



@socketio.on('connect',namespace='/getimages')
def onconnect():
    #creating single user when a request comes and 
    #allocate resources to request
    #print(request.sid)
    new_user = User()
    session['id'] = request.sid
    #print(session['id'])
    #user list 
    #key: the id of the class and value is the actual class
    #because session do json conversion of the object
    all_users[request.sid] = new_user
    print('user connected') 
    socketio.emit('onconnect','user connected',namespace='/getimages')

@socketio.on('disconnect',namespace='/getimages')
def ondisconnect():
    print(request.sid ," got deleted")

    if request.sid in all_users:
        del all_users[request.sid]

    print('\nUser disconnected\n')
    
@flask_app.route('/')
@flask_app.route('/images')
def start():
    return render_template("gimage.html")

@socketio.on('query',namespace='/getimages')
def get_query(query):
    if query:
        #getting the query
        query = query['query']
        print('query is ',query)
        print(session['id'])
        #if sessio which is always there on first connection
        if session:
            sid = session['id']
            all_users[sid].start_browser()
            print(all_users[sid].browser)
        else:
            print('id not in seesion')

        search_query(query)
        socketio.emit('query_recv',"received",namespace='/getimages')
        #start_scrapper()
        #next_link = get_image_link()
        #print(session['user'])
        #session['next_link'] = get_image_link()
        #print(session['next_link'])
        #print(type(session['next_link']))
        #query = request.form['query']
        #print(query)
        #what is query
        #session['query'] = query


def download_link(link):
    data = requests.get(link)
    total_chunk = ''
    with open('temp.txt','wb+') as f:
        for chunk in data.iter_content(chunk_size=3048):
            f.write(chunk)
        f.seek(0)
        total_chunk = f.read()
        return base64.encodebytes(total_chunk)


@flask_app.route('/getlink')
def get_link():
    try:
        all_links = []
        total_images = 5
        for i in range(0,total_images):
            next_image_link =  next(next_link)
            print(next_image_link)
            #all_links.append(next_image_link)

    except StopIteration:
        return "that's all we have",404

@socketio.on('getlink',namespace='/getimages')
def getlink(message):
    try:
        print(message)
        print(type(message))
        total_images = message["images"]
        for i in range(0,total_images):
            this_user = all_users[session['id']]
            next_image_data =  next(this_user.next_link)
            #print(next_image_data)
            #print(type(next_image_data))
            next_image_data['data'] = download_link(next_image_data['link']).decode('utf-8')
            next_image_data['image_name'] = Image_Name(next_image_data['link'])
            socketio.emit('getimage',next_image_data,namespace = '/getimages')
            #print(next_image_data)
    except StopIteration:
        return "that's all we have",404