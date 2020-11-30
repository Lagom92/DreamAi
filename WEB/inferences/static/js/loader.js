$(window).load(function(){
    $('#loading').delay('300').fadeOut()
    console.log("loading....")

})

function loading(){
    $("#loading").show();
    $("#loader_text").show();

    $(".body").hide(); 
}