var timerId
$(document).ready(function() {

    $("#cancel_btn").click(function(){
        var reset = confirm("Это действие приедёт к сбросу теста, вы уверены?");
        if (reset){
            $(location).attr('href','/demonstrator/upload/')
        }
    });

    $("#control_btn").click(function(){
        if($(this).html() == 'Запустить тестирование'){
            $(this).html('Приостановить тестирование').removeClass('btn-success').addClass('btn-primary');
            $("#navbar-text").html('Идёт тестирование').css({'color':'red'});
            $('#question').load('/demonstrator/_new_question/');
            quest_num = Number($('#question').attr("quest-num"));
            $('#question').attr("quest-num", quest_num+1)
            timerId = setInterval(interval, 10);
        } else if ($(this).html() == 'Продолжить тестирование'){
            $(this).html('Приостановить тестирование').removeClass('btn-success').addClass('btn-primary');
            $("#navbar-text").html('Идёт тестирование').css({'color':'red'});
            timerId = setInterval(interval, 10);
        } else {
            $(this).html('Продолжить тестирование').removeClass('btn-primary').addClass('btn-success');
            $("#navbar-text").html('Тестирование приостановлено').css({'color':'black'});
            clearInterval(timerId);
        }
    });


});

function interval(){
    var now = Number($(".progress-bar").attr("aria-valuenow"));
    var start = Number($(".progress-bar").attr("aria-valuemin"));
    var end = Number($(".progress-bar").attr("aria-valuemax"));
    if (now == end) {
        quest_num = Number($('#question').attr("quest-num"));
        quest_max = Number($('#question').attr("quest-max"));
        if (quest_max == quest_num) {
            var audio=new Audio();
            audio.src='/static/sound.mp3';
            audio.play();

            $(location).attr('href','/demonstrator/test_finish/')
        } else {
            var audio=new Audio();
            audio.src='/static/sound.mp3';
            audio.play();
            $('#question').load('/demonstrator/_new_question/');
            now=0;
        }
        $('#question').attr("quest-num", quest_num+1)
    }
    $(".progress-bar").attr("aria-valuenow",now+1);
    $(".progress-bar").attr("style","width:"+now/end*100+"%; transition:none;");

}