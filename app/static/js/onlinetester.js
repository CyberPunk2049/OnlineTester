var timerId
$(document).ready(function() {

    $("#cancel_btn").click(function(){
        alert("Это действие приедёт к сбросу теста, вы уверены?");
    });

    $("#control_btn").click(function(){
        if($(this).html() == 'Запустить тестирование'){
            $(this).html('Приостановить тестирование')
            $('#question').load('/demonstrator/_new_question/');
            quest_num = Number($('#question').attr("quest-num"));
            $('#question').attr("quest-num", quest_num+1)
            timerId = setInterval(interval, 10);
        } else if ($(this).html() == 'Продолжить тестирование'){
            $(this).html('Приостановить тестирование')
            timerId = setInterval(interval, 10);
        } else {
            $(this).html('Продолжить тестирование')
            clearInterval(timerId)
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
            $(location).attr('href','/demonstrator/test_finish/')
        } else {
            $('#question').load('/demonstrator/_new_question/');
            now=0;
        }
        $('#question').attr("quest-num", quest_num+1)
    }
    $(".progress-bar").attr("aria-valuenow",now+1);
    $(".progress-bar").attr("style","width:"+now/end*100+"%; transition:none;");

}