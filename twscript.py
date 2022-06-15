import tweepy
import os
import json
import sys
from geopy.geocoders import Nominatim
from database import Tweet, User

api = None
def init_api():
   global api
   auth = get_auth()
   api = tweepy.API(auth)

def get_auth():
   consumer_key = 'APIKEY'
   consumer_secret = 'APIKEY'
   access_token = 'APIKEY'
   access_token_secret = 'APIKEY'
   auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
   auth.set_access_token(access_token, access_token_secret)
   return auth

def get_tweets(usuario):
   tweets = api.user_timeline(screen_name=usuario.twnick, 
                           count=200,
                           include_rts = False,
                           tweet_mode = 'extended'
                           )
   for info in tweets[:50]:
     ubi= ubi_from_tweet(info.id)
     coord= 'None'
     if ubi != 'None':
        coord = get_ubi(ubi)
     tw = Tweet.create_or_update({'text':info.full_text, 'id_tw':info.id, 'location':ubi, 'geo': coord, 'date': info.created_at})[0]
     tw.author.connect(usuario)

   return usuario.tweets

def ubi_from_tweet(id):
      nombre="None"
      status = api.get_status(id)
      if(status.place is not None):
         nombre=status.place.full_name
      return nombre

def get_user(userID):
   user = api.get_user(screen_name=userID)
   name = user.name
   place = user.location
   description = user.description
   pimage = user.profile_image_url_https
   pbanner = user.profile_banner_url
   friends = user.friends_count
   coord= 'None'
   if place != 0:
      coord = get_ubi(place)
   
   usuario = User.create_or_update({'twnick': userID, 'fullname':name, 'location':place, 'description':description, 'tw_profile_image_url':pimage, 'tw_profile_banner_url':pbanner, 'geo':coord})
   return User.nodes.filter(twnick=userID)[0]

def get_ubi(place):
   geolocator = Nominatim(user_agent="bea")
   location = geolocator.geocode(place)
   if(location!=None):
      print("Ciudad: " + str(location) + "\nCoordenadas " , (location.latitude, location.longitude))
      return (location.latitude, location.longitude)


def get_trends(coordenadas):
   lista=api.closest_trends(coordenadas[0], coordenadas[1])
   trends = api.get_place_trends(id = lista[0]['woeid'])

   print("Trending Topics para", coordenadas, "----------")
   for i in range(0,len(trends[0]['trends'])):
      print(trends[0]['trends'][i]['name'],", ", end = ' ') 

if __name__ == '__main__':
   username = "nombre_de_usuario"
   print("Extractor de Tweets ---------------------------------------")
   init_api()

   get_user(username)
   user= User.nodes.filter(twnick=username)[0]
   print(user)
   if len(user.location) != 0:
      coordinates= get_ubi(user.location)
      get_trends(coordinates)
   get_tweets(user)