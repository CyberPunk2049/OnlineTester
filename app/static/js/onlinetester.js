var timerId
$(document).ready(function() {

    $("#cancel_btn").click(function(){
        alert("Это действие приедёт к сбросу теста, вы уверены?");
    });

    $("#control_btn").click(function(){
        if($(this).html() == 'Запустить тестирование'){
            $(this).html('Приостановить тестирование')
            timerId = setInterval(interval, 10);
        } else {
            $(this).html('Запустить тестирование')
            clearInterval(timerId)
        }
        console.log(timerId)
    });


});

function interval(){
    var now = Number($(".progress-bar").attr("aria-valuenow"));
    var start = Number($(".progress-bar").attr("aria-valuemin"));
    var end = Number($(".progress-bar").attr("aria-valuemax"));
    if (now == end){
        $('.row').load('/demonstrator/_new_question/');
        now=0;
    }
    $(".progress-bar").attr("aria-valuenow",now+1);
    $(".progress-bar").attr("style","width:"+now/end*100+"%; transition:none;");

}