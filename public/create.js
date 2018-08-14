$(document).ready(function() {

$(".submit").click(function(e) {
  $.post("/submit", {"text": $("input[name='input']").val()})
    .done(function(string) {
      $("#result").show();
      $("#result").html("<a href='" + window.location.protocol + "//" + window.location.hostname + ":"
                        + window.location.port+ "/message?id=" + string + "'>" + window.location.hostname + ":"
                        + window.location.port+ "/message?id=" + string +"</a>");
    });
  e.preventDefault();
});

});