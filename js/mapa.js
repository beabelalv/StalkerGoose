var map;
console.log(posts)
var geo = ("39.56503921793444, -3.543409575108961").split(",");
if (user['geo'] != 'None'){
    var geo = user['geo'].slice(1,-1).split(",");
}

function twInfo(){
    var posicion = new google.maps.Marker;
    document.getElementById('nombre').innerHTML = user['fullname'];
    document.getElementById('resultado').innerHTML = user['twnick'];
    document.getElementById('location').innerHTML = user['location'];
    document.getElementById('description').innerHTML = user['description'];

    var img=document.createElement("img");
    img.src = user['tw_profile_image_url'];
    var src = document.getElementById('fototw');
    src.appendChild(img);

    var tweetsByLocation = tweets.reduce((acc,tweet)=>{
        var loc = tweet.location;
        if (acc[loc]===undefined){
            acc[loc]=[tweet]
        }else{
            acc[loc]=[...acc[loc],tweet]
        }
        return acc;
    }, {})

    return tweetsByLocation;
}

function instaInfo(){
    var posicion = new google.maps.Marker;
    document.getElementById('nombreinsta').innerHTML = instauser['fullname'];
    document.getElementById('resultado2').innerHTML = instauser['instaNick'];
    document.getElementById('descriptioninsta').innerHTML = instauser['description'];
    //document.getElementById('urlinsta').innerHTML = instauser['url'];
    //console.log("posts", posts);
    var postsByLocation = posts.reduce((acc,post)=>{
        var loc = post.location;
        if (acc[loc]===undefined){
            acc[loc]=[post]
        }else{
            acc[loc]=[...acc[loc],post]
        }
        return acc;
    }, {})
    return postsByLocation;
}


function initMap() { 
    markers=[];
    //Ajustes con los que quiero que se vea el mapa
    var options = {
        center: {lat: parseFloat(geo[0]), lng: parseFloat(geo[1])},
        zoom: 7,
        disableDefaultUI: true,
        zoomControl: true
    }

    map = new google.maps.Map(document.getElementById('map'), options);
    tweetsByLocation = twInfo();
    //console.log("location tweets",tweetsByLocation);
    addAllMarkers(tweetsByLocation);
    postsByLocation = instaInfo();
    addAllMarkersInstagram(postsByLocation);
    //console.log(postsByLocation)
    }  

function myPosition(latitud, longitud){
    var marker = new google.maps.Marker({
        title: "Tu posición actual",
        position: {lat: latitud, lng: longitud},
        map:map,
        icon : "src/markers/tuposicion1.png"
    });

    markers.push(marker);
}

function addMarker(location, geo, datos_tweet){
    var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
    var marker = new google.maps.Marker({
        position: {lat: parseFloat(geo[0]), lng: parseFloat(geo[1])},
        place_name : location,
        map:map
    });
    marker.setIcon("src/tw.png");
    marker.addListener('click', function(){
            $("#move").animate({right: '-70%' });
            $("#move").animate({ right: '1%', }); 

            setTimeout(function(){
                document.getElementById('text-more-info').innerHTML = "Últimos tweets para la ubicación:";
                document.getElementById('text-title').innerHTML = location;
                var src = document.getElementById('tweets');
                var src2 = document.getElementById('tweets');

                src.innerHTML = ""
                for(i=0; i<datos_tweet.length;i++){
                    var div = document.createElement('div');
                    div.innerHTML = datos_tweet[i]['text'];
                    src.appendChild(div);
                    div.classList.add("twdiv")
                    var div2 = document.createElement('div');
                    div2.innerHTML = datos_tweet[i]['date'];
                    div2.classList.add("fechadiv")
                    src.appendChild(div2);
                }
            }, 300); }); }
            
function addAllMarkers(TweetsByLocation){
    datos = Object.keys(TweetsByLocation)
    for (var i=0; i<datos.length; i++){
        var coordinates = TweetsByLocation[datos[i]][0]['geo']
        if(coordinates != 'None'){
            var primer_tweet = TweetsByLocation[datos[i]][0]
            var place_name=  primer_tweet['location']
            coordinates =  primer_tweet['geo'].slice(1,-1).split(",");
            datos_contenido = TweetsByLocation[datos[i]]
            addMarker(place_name, coordinates, datos_contenido);
        }
    }
}

function addInstagramMarker(location, geo, datos_contenido){
    var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
    var marker = new google.maps.Marker({
        position: {lat: parseFloat(geo[1]), lng: parseFloat(geo[0])},
        place_name : location,
        map:map
    });
    marker.setIcon("src/instagram.png");
    marker.addListener('click', function(){
        $("#move").animate({right: '-70%' });
        $("#move").animate({ right: '1%', }); 

        setTimeout(function(){
            document.getElementById('text-more-info').innerHTML = "Últimos posts para la ubicación:";
            document.getElementById('text-title').innerHTML = location;
            var src = document.getElementById('tweets');
            var src2 = document.getElementById('tweets');

            src.innerHTML = ""
            for(i=0; i<datos_contenido.length;i++){
                var div = document.createElement('div');
                div.innerHTML = datos_contenido[i]['text'];
                src.appendChild(div);
                div.classList.add("twdiv")
                var div2 = document.createElement('div');
                div2.innerHTML = datos_contenido[i]['date'];
                div2.classList.add("fechadiv")
                src.appendChild(div2);

                var div3 = document.createElement('div');
                div3.innerHTML = datos_contenido[i]['url'];
                div3.classList.add("enlacediv")
                src.appendChild(div2);
            }
        }, 300); });
};

function addAllMarkersInstagram(PostsByLocation){
    datos = Object.keys(PostsByLocation)
    for (var i=0; i<datos.length; i++){
        var coordinates = PostsByLocation[datos[i]][0]['geo']
        if(coordinates != 'none'){
            var primer_post = PostsByLocation[datos[i]][0];
            var place_name=  primer_post['location'];
            coordinates =  primer_post['geo'].slice(1,-1).split(",");
            var datos_contenido = PostsByLocation[datos[i]];
            //(place_name, coordinates, datos_contenido);  
            addInstagramMarker(place_name, coordinates, datos_contenido);
        }
    }
}





