import base64
from logging import exception
import os
import json
import codecs
from instagram_private_api import Client, ClientCompatPatch, ClientError
from numpy import DataSource
import requests
import io
from database import Insta, Pic
from datetime import datetime

user_name = 'Inserta tu nombre de usuario'
password = 'Inserta tu contraseña'
settings_file = 'settings.json'

def on_login_callback(api):
    with open(settings_file, 'w') as file:
        settings=api.settings
        settings['cookie'] = codecs.encode(settings['cookie'], 'base64').decode()
        json.dump(settings, file)

def createUser(username, api):
    nombre = api.username_info(username)['user']['full_name']
    privado = api.username_info(username)['user']['is_private']
    bio = api.username_info(username)['user']['biography']
    image = api.username_info(username)['user']['profile_pic_url']
    url = api.username_info(username)['user']['external_url']
    insta = Insta.create_or_update({'instaNick':username, 'fullname':nombre, 'description':bio, 'profile_image_url': image, 'url': url})[0]

    return Insta.nodes.filter(instaNick=username)[0]

def createPosts(usuario, api): 
    username = usuario.instaNick
    datos = api.username_info(username)  
    user_id=str(datos['user']['pk'])
    texto = api._call_api('users/'+user_id+'/full_detail_info/')    

    posts = texto["feed"]["items"]
    for i in range(len(posts)):  
        id_foto = posts[i]['pk']
        pie_de_foto = str(posts[i]["caption"]["text"]) if posts[i]["caption"] != None else "none"
        timestamp = posts[i]["taken_at"]
        dt_object = str(datetime.fromtimestamp(timestamp))
        location =  str(posts[i]["location"]["name"]) if "location" in posts[i] else "none"
        geo = ("(" + str(posts[i]["location"]["lng"]) + "," + str(posts[i]["location"]["lat"]) +")") if "lng" in posts[i] else "none"
        
        post = Pic.create_or_update({'id_foto':id_foto, 'text':pie_de_foto, 'location':location, 'geo': geo, 'date': dt_object})[0]
        post.author.connect(usuario)

def creating_users(username):
    try:
        if os.path.isfile(settings_file):
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data)
                cached_settings['cookie']= codecs.decode(cached_settings['cookie'].encode(), 'base64')

                api = Client(user_name, password, on_login=on_login_callback, settings=cached_settings)
                usuario = createUser(username, api)
                createPosts(usuario, api)
                print("Se han creado los posts")
                
        else: 
            api = Client(user_name, password, on_login=on_login_callback)

        results = api.feed_timeline()
        items = results.get('items', [])
  
    except ClientError as error:
        print("Please follow this link to complete the challenge: " + error.challenge_url)

    return api

if __name__ == "__main__":
    creating_users("nombre_de_usuario")