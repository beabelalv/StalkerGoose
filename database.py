from xml.dom.minidom import TypeInfo
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config, cardinality

config.DATABASE_URL = 'bolt://neo4j:bea@localhost:7687'

class Tweet(StructuredNode):
    id_tw = StringProperty(unique_index=True, required=True)
    text = StringProperty()
    author = RelationshipTo('User', 'WRITTEN_BY')
    location = StringProperty()
    geo = StringProperty()
    date = StringProperty()

class User(StructuredNode):
    twnick = StringProperty(unique_index=True, required=True)
    fullname = StringProperty()
    location = StringProperty()
    description = StringProperty()
    tw_profile_image_url = StringProperty()
    tw_profile_banner_url = StringProperty()
    tweets = RelationshipFrom('Tweet', 'WRITTEN_BY')
    geo = StringProperty()

class Insta(StructuredNode):
    instaNick = StringProperty(unique_index=True, required=True)
    fullname = StringProperty()
    description = StringProperty()
    profile_image_url = StringProperty()
    pic = RelationshipFrom('Pic', 'POSTED_BY')
    

class Pic(StructuredNode):
    id_foto = StringProperty(unique_index=True, required=True)
    text = StringProperty()
    author = RelationshipTo('Insta', 'POSTED_BY')
    location = StringProperty()
    geo = StringProperty()
    date = StringProperty()
