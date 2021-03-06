$(document).ready(function(){

    var timerId = setTimeout(function check() {


        var data = {
            location: document.location.pathname
        };

        if (document.location.pathname == '/studentstester/test_process/') {
            data['quest_num'] = $("#question").attr('value')
        }

    // Производится регулярный опрос сервера, для того чтобы понять, актуальна ли данная страница текущему состоянию,
    // если страница не актуальна, производится полная перезагрузка страницы.
        $.ajax({
            type: 'GET',
            data: data,
            dataType: 'JSON',
            success: function (json) {
                console.log(json.reload)
                if (json.reload) {
                    console.log(json.reload)
                    if (document.location.pathname = '/studentstester/test_process/'){
                        var data = save_answer()
                        $.ajax({
                            type: 'PUT',
                            data: data,
                            success: function () {
                                document.location.reload()
                                blink()
                            },
                            error: function () {
                                timerId = setTimeout(check,1000)
                            }
                        })
                    } else {
                        document.location.reload()
                    }


                } else {
                    timerId = setTimeout(check,1000);
                }
            },
            error: function () {
                alert("Соединение утеряно, нажмите ОК, чтобы проверить ещё раз!");
                timerId = setTimeout(check,1000)
            }
        })

    }, 1000);

    //На странице выбора варианта устанавливаются обработчики кликов на кнопки с вариантами
    $(".button_variant1").click(click_variant);
    $(".button_variant2").click(click_variant);


    //Обработчик клика по кнопке отмены регистрации на тестирвоание
    $("#cancel_btn").click(function () {
        var reset = confirm("Вы уверены что хотите отменить регистрацию на тестирование?");
        if (reset){
            $.ajax({
                type: 'DELETE',
            })
        }
    });

    //Устанавливаются обработчики кликов на кнопки с ответами на тест вкл/выкл
    $(".button_answ").click(function(){
        if ($(this).hasClass("button_answ_off")) {
            $(this).removeClass('button_answ_off').addClass('button_answ_on');
        } else if ($(this).hasClass("button_answ_on")) {
            $(this).removeClass('button_answ_on').addClass('button_answ_off');
        }

    });

});

//Функция сохраняет выбранный вариант
function click_variant() {
        $.ajax({
        type: 'PUT',
        data: {
            location: document.location.pathname,
            variant: $(this).attr("value")
        }
    })
};

//Функция сохраняет текущее состояние ответов на вопрос
function save_answer() {
    var data = {
        location: document.location.pathname,
        quest_num: $("#question").attr("value")
    };
    $(".button_answ").each(function (i) {
        if ($(this).hasClass("button_answ_on")){
            data['answer_'+i] = "True"
        } else {
            data['answer_'+i] = "False"
        }
    });
    console.log(data);
    return data
}

//Функция на короткое время делает фон экрана белым
function blink() {
    $("body").addClass('blink').
    setTimeout(function () {
        $("body").removeClass('blink')
    }, 1000)

}