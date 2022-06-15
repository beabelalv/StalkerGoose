$(document).ready(main);

var flag = 0;

function main (){
    
    $('.btn-menu').click(function(){
        if(flag==0){
            
            flag=1;
            
            $("#floating-panel").animate({
                    left: '1%'                        
                });
            
            $("#floating-panel-right").animate({
                    right: '-100%'                        
                });
            
            
            $('.menu-bar').animate({
                    left: '-120%'                         
                });
            
        }
    });
    
    $('.btn-click').click(function(){
        flag=0;

            $("#floating-panel").animate({
                    left: '-120%'                        
                });

            $('.menu-bar').animate({
                left: '1%'                   
            });
    });

    $('.btn-click-1').click(function(){
            $("#move").animate({
                    right: '-100%'                        
                });
    });
};

