var timerId
$(document).ready(function() {
    timerId = setInterval(interval, 10);

    $("#control_btn").click(function(){
        if ($(this).html() == 'Приостановить тестирование'){
            $(this).html('Продолжить тестирование').removeClass('btn-primary').addClass('btn-success');
            $("#navbar-text").html('Тестирование приостановлено').css({'color':'black'});
            clearInterval(timerId);
        } else {
            $(this).html('Приостановить тестирование').removeClass('btn-success').addClass('btn-primary');
            $("#navbar-text").html('Идёт тестирование').css({'color':'red'});
            timerId = setInterval(interval, 10);
        }
    });


    $("#cancel_btn").click(function(){
        var reset = confirm("Это действие приедёт к сбросу теста, вы уверены?");
        if (reset){
            $(location).attr('href','/demonstrator/upload/')
        }
    });

    // Устанавливается интервал для вызова функции обновления числа участников на странице регистрации на тестирование
    if (document.location.pathname == '/demonstrator/test_registration/') {
        var registerTimerId = setInterval(students_update, 1000);
    }

    //Устанавливается обработчик кликов на строке таблице со списком выполненных тестов
    $("#tests tr").click(function () {
       if (this.getAttribute("id") != null){
           var id = this.getAttribute("id")
           document.location.assign(document.location.origin+'/estimator/test_results/?'+'test_id='+id+'&full_answer='+1)
       }
    });

    //Устанавливается обработчик кликов на строке таблице со списком выполненных тестов
    $("#results tr").click(function () {
       if (this.getAttribute("id") != null){
           var id = this.getAttribute("id")
           document.location.assign(document.location.origin+'/estimator/student_answers/?'+'student_id='+id)
       }
    });

    // Устанавливается обработчик кликов на radio на страние результатов теста
    $("[name='answertype'] input").click(function () {
        document.location.assign(document.location.origin+'/estimator/test_results/?'
            +'test_id='+$("[name='answertype']").attr("test_id")
            +'&full_answer='+$("[name='answertype'] input:checked").val())
    })

    // Устанавливается обработчик кликов на кнопке "Назад" в результатах
    $("#back_btn").click(function () {
        if (document.location.pathname == "/estimator/tests_list/") {
            document.location.assign(document.location.origin+'/administrator/')
        } else if (document.location.pathname == "/estimator/test_results/") {
            document.location.assign(document.location.origin+'/estimator/tests_list/')
        } else if (document.location.pathname == "/estimator/student_answers/") {
            var test_id = $("#results").attr("test_id")
            document.location.assign(document.location.origin+'/estimator/test_results/?'+'test_id='+test_id+'&full_answer='+1)
        }
    })

    // Устанавливается обработчик кликов на кнопке "Очистить список"
    $("#clear_btn").click(function () {
        var clear = confirm("Вы уверены что хотите очистить список завершённых тестов по данному предменту?");
        if (clear) {
            $.ajax({
                type:'DELETE',
                success: function () {
                    document.location.reload()
                },
                error: function () {
                    alert("Не удаётся почитстить список, попробуйте ещё раз!")
                }
                
            })
        }
    })

});

function interval(){
    var now = Number($(".progress-bar").attr("aria-valuenow"));
    var start = Number($(".progress-bar").attr("aria-valuemin"));
    var end = Number($(".progress-bar").attr("aria-valuemax"));
    if (now == end) {
        var quest_num = Number($('#question').attr("quest-num"));
        var quest_max = Number($('#question').attr("quest-max"));
        if (quest_max == quest_num) {
            var audio = new Audio();
            audio.src = '/static/sound.mp3';
            audio.play();

            $(location).attr('href', '/demonstrator/test_finish/')
        } else {
            var audio = new Audio();
            audio.src = '/static/sound.mp3';
            audio.play();
            $('#question').load('/demonstrator/_new_question/');
            now = 0;
        }
        $('#question').attr("quest-num", quest_num + 1)
    }
    $(".progress-bar").attr("aria-valuenow",now+1);
    $(".progress-bar").attr("style","width:"+now/end*100+"%; transition:none;");

}

function students_update() {
    //Функция обновляет число зарегистрировавшихся на тестирование участников
    console.log('load');
    $('#studentscount').load('/demonstrator/_students_count/');
}