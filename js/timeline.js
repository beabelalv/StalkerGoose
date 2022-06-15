twitter_timeline();
insta_timeline();


function twitter_timeline(){


    for (var i=0; i<tweets.length; i++){
        var src = document.getElementById('contenidotw');

        var contenedordiv = document.createElement('div');
        src.appendChild(contenedordiv);
        contenedordiv.setAttribute('id', 'contenedor-tweet');

        src = contenedordiv
        
        var img=document.createElement("img");
        img.src = user['tw_profile_image_url'];
        src.appendChild(img);
        
        var div = document.createElement('div');
        div.innerHTML = tweets[i]['text'];
        src.appendChild(div);
        div.classList.add("twdiv");
        
        var div2 = document.createElement('div');
        div2.innerHTML = (tweets[i]['date']).slice(0, -6);
        div2.classList.add("fechadiv")
        src.appendChild(div2);

        var div3 = document.createElement('div');
        div3.innerHTML = tweets[i]['url'];
        div3.classList.add("enlacediv")
        src.appendChild(div2);
        
        console.log(tweets[i]);
    }

}


function insta_timeline(){


    for (var i=0; i<posts.length; i++){

        var src = document.getElementById('contenidoinsta');

        var contenedordiv = document.createElement('div');
        src.appendChild(contenedordiv);
        contenedordiv.setAttribute('id', 'contenedor-tweet');

        src = contenedordiv
        
        insta_username = instauser['instaNick']; 

        var img=document.createElement("img");
        img.src = "src/pfpics/pfpic-"+insta_username+".jpg";
        src.appendChild(img);
        
        var div = document.createElement('div');
        div.innerHTML = posts[i]['text'];
        src.appendChild(div);
        div.classList.add("twdiv");
        
        var div2 = document.createElement('div');
        div2.innerHTML = (posts[i]['date']);
        div2.classList.add("fechadiv")
        src.appendChild(div2);

        var div3 = document.createElement('div');
        div3.innerHTML = posts[i]['url'];
        div3.classList.add("enlacediv")
        src.appendChild(div2);

        /*
        var div = document.createElement('div');   
        div.innerHTML = posts[i]['text'];
        src.appendChild(div);
        div.classList.add("twdiv");

        var div2 = document.createElement('div');
        div2.innerHTML = posts[i]['date'];
        div2.classList.add("fechadiv")
        src.appendChild(div2);

        var div3 = document.createElement('div');
        div3.innerHTML = posts[i]['url'];
        div3.classList.add("enlacediv")
        src.appendChild(div2);

        console.log(posts[i]);*/
    }

}