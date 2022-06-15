import folium
import webbrowser
import twscript
import tweepy
from database import Tweet, User
from neomodel import Q
from instagram import creating_users
from database import Insta
import urllib.request

def tweets_marker(user):
    tweets = twscript.get_tweets(user)
    print("Imprimir tweets")
    return tweets

def tweets_mapa(username):
    twscript.init_api()
    user = twscript.get_user(username)
    if user.geo == None:
        user.geo = 'None'
        
    coordinates = twscript.get_ubi(user.location)
    tweets= tweets_marker(user)
    array = "["
    for tweet in tweets:
        array += str(tweet) + ","
    array = array[:-1]
    array += "]"

    return [user,array]

def insta_mapa(username_insta):
    usuario = Insta.nodes.filter(instaNick=username_insta)[0]
    fotos = usuario.pic
    perfil = usuario.profile_image_url
    urllib.request.urlretrieve(perfil, "src/pfpics/pfpic-"+username_insta+".jpg")
    array_insta="["
    print(fotos)
    if (len(fotos) == 0):
        array_insta=[]
    else:
        for elemento in fotos:
            array_insta += str(elemento) + ","
        array_insta = array_insta[:-1]
        array_insta += "]"
    return [usuario, array_insta]

if __name__ == '__main__':
    print("""                                                        _...--.
                                        _____......----'     .'
                                  _..-''                   .'
                                .'                       ./
                        _.--._.'                       .' |
                     .-'                           .-.'  /
                   .'   _.-.                     .  \   '
                 .'  .'   .'    _    .-.        / `./  :
               .'  .'   .'  .--' `.  |  \  |`. |     .'
            _.'  .'   .' `.'       `-'   \ / |.'   .'
         _.'  .-'   .'     `-.            `      .'
       .'   .'    .'          `-.._ _ _ _ .-.    :
      /    /o _.-'   Stalker     .--'   .'   \   |
    .'-.__..-'        Goose     /..    .`    / .'
  .'   . '                       /.'/.'     /  |
 `---'                                   _.'   '
                                       /.'    .'
                                        /.'/.'""")
    username=input("Introduzca el nickname de Twitter: ")
    username_insta = input("Introduzca el nickname de Instagram: ")
    
    creating_users(username_insta)

    array=tweets_mapa(username)
    array_insta=insta_mapa(username_insta)

    instaUser = Insta.nodes.filter(instaNick=username_insta)[0]

    with open('mapa.html','r', encoding="utf-8") as f:
        lines = f.readlines()

    with open('mapa.html','w', encoding="utf-8") as f:
        for line in lines:
            if line.startswith('        var user= '):
                line = str('        var user= '  + str(array[0]) +  ";\n")

            if line.startswith('        var tweets='):
                line = str('        var tweets=' + array[1] +  ";\n")

            if line.startswith("        var instauser= "):
                line = str("        var instauser= "+ str(array_insta[0]) +  ";\n")

            if line.startswith("        var posts= "):
                line = str("        var posts= "+ str(array_insta[1]) +  ";\n")                
            f.write(line)
    
    with open('timeline.html','r', encoding="utf-8") as f:
        lines = f.readlines()

    with open('timeline.html','w', encoding="utf-8") as f:
        for line in lines:
            if line.startswith('        var user= '):
                line = str('        var user= '  + str(array[0]) +  ";\n")

            if line.startswith('        var tweets='):
                line = str('        var tweets=' + array[1] +  ";\n")

            if line.startswith("        var instauser= "):
                line = str("        var instauser= "+ str(array_insta[0]) +  ";\n")

            if line.startswith("        var posts= "):
                line = str("        var posts= "+ str(array_insta[1]) +  ";\n")                
            f.write(line)

    webbrowser.open("mapa.html")   
