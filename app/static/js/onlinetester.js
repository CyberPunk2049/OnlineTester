$(document).ready(function() {
    $("#cancel_btn").click(function(){
        alert("Это действие приедёт к сбросу теста, вы уверены?");
    });
    var timerId = setInterval(function() {
        var now = Number($(".progress-bar").attr("aria-valuenow"));
        var start = Number($(".progress-bar").attr("aria-valuemin"));
        var end = Number($(".progress-bar").attr("aria-valuemax"));

        $(".progress-bar").attr("aria-valuenow",now+1);
        $(".progress-bar").attr("style","width: "+now/end*100+"%");
    }, 100);
});