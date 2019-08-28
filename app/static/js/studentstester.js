$(document).ready(function(){

    setInterval(function () {
        $.ajax({
            type: 'GET',
            data: {
                ajax: 'True',
            },
            dataType:'JSON',
            success:function(json){
                if (json.reload){
                    document.location.reload()
                }
            }
            })
    }, 500);

    $(".variant").click(function () {
        console.log($(this).attr("value"))
        $.ajax({
            type: 'PUT',
            data: {
                ajax:'True',
                variant: $(this).attr("value")
            }
        })
    });

    $("#cancel_btn").click(function () {
        var reset = confirm("Вы уверены что хотите отменить регистрацию на тестирование?");
        if (reset){
            $.ajax({
                type: 'DELETE',
            })
        }
    });
});