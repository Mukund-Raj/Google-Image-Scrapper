from app import flask_app,socketio
from flask import render_template,request,jsonify,session
from app.gimage import start_scrapper,get_image_link,search_query,total_images
from app.Image_File_Name import Image_Name
import base64
import requests

next_link = None

@socketio.on('connect',namespace='/getimages')
def onconnect():
    socketio.emit('onconnect','user connected',namespace='/getimages')

@flask_app.route('/')
@flask_app.route('/images')
def start():
    #global next_link
    #start_scrapper()
    #next_link = get_image_link()
    return render_template("gimage.html")


@flask_app.route('/query',methods=['POST'])
def get_query():
    if request.method == 'POST':
        if request.form:
            if 'query' not in session:
                global next_link
                start_scrapper()
                next_link = get_image_link()
                query = request.form['query']
                print(query)
                #what is query
                #session['query'] = query
                search_query(query)
            else:
                if session['query'] != request.form['query']:
                    pass

            return "Got it",200

    return "Not Found",404


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
            next_image_data =  next(next_link)
            next_image_data['data'] = download_link(next_image_data['link']).decode('utf-8')
            next_image_data['image_name'] = Image_Name(next_image_data['link'])
            socketio.emit('getimage',next_image_data,namespace = '/getimages')
            #print(next_image_data)
    except StopIteration:
        return "that's all we have",404