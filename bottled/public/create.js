$(document).ready(function() {

$(".submit").click(function(e) {
  $.post("/submit", {"text": $("textarea[name='input']").val()})
    .done(function(string) {
      $("#left").addClass("close");
      $("#right").addClass("close");
      $("#text").addClass("close");
      $("#result").addClass("show");
      $("#link").html("<a href='" + window.location.protocol + "//" + window.location.hostname + ":"
                        + window.location.port+ "/message?id=" + string + "'>" + window.location.hostname + ":"
                        + window.location.port+ "/message?id=" + string +"</a>");
    });
  e.preventDefault();
});

});