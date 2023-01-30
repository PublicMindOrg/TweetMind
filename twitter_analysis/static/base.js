$(document).ready(function(){
    $("input").click(function(){
        let src = ''
        let c_name = $(this).attr('id');
        if (c_name=='btnradio1'){
            src = '/static/tweets_per_day.png'
        }
        else if (c_name=='btnradio2'){
            src = '/static/best_model_cm.png'
        }
        else {
            src = '/static/hour_created.png'
        }
        $("#analysis").css("display", "block");
        $('#analysis-1').attr("src", src);
    });
  });